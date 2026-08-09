/*
============================================================
NorthStar Commerce

File:
18_customer_purchase_health_engine.sql

Purpose:
Creates the NorthStar Customer Purchase Health Engine by 
calculating personalized purchasing behavior, Purchase 
Health Scores, and Purchase Health Tiers for every 
customer. This engine serves as the analytical foundation
for subsequent customer intelligence reports throughout 
NorthStar Commerce.

Business Question:
Which customers appear healthy, which should be
monitored, and which may require retention efforts
based on changes in their normal purchasing behavior?

Business Context:
This query introduces the NorthStar Customer Purchase
Health Engine, a reusable analytical model designed to
support customer retention, revenue analysis, customer 
lifetime value, and future customer intelligence reports.

Rather than using a single fixed inactivity threshold,
each customer is evaluated against their own historical
purchase frequency.

The model establishes an average purchase interval,
applies a 20% healthy grace period, measures how far
the customer has moved beyond that personalized window,
and converts the deviation into a standardized
Purchase Health Score.

The resulting score is translated into a business-friendly
Purchase Health Tier so NorthStar can identify customers
who may benefit from proactive retention efforts.

Metrics Used:
- Average Days Between Purchases
- Last Purchase Date
- Successful Order Count
- One-Time vs. Repeat Customer Classification
- Days Since Last Purchase
- Days Beyond or Within Average
- Grace Period Days
- Healthy Window Days
- Days Beyond Healthy Window
- Percent Beyond Healthy Window
- Purchase Health Score

Purchase Health Tiers:
- Healthy: 95-100
- Watch: 80-94.99
- At Risk: 60-79.99
- Critical: 0-59.99
- Insufficient History: No usable purchase interval

Expected Output:
One row per customer including historical purchase
behavior, current purchase state, personalized health
metrics, Purchase Health Score, and Purchase Health Tier.

Model Notes:
- Customers remain fully Healthy throughout their
  personalized healthy window.
- Health scores decline linearly after the healthy
  window is exceeded.
- Scores are bounded between 0 and 100.
- One-time customers and customers with a zero-day
  average purchase interval are classified as
  Insufficient History for scoring purposes.

Revision History:
------------------------------------------------------------
Version 1.0 (2026-08-07)
- Initial release
- Introduced personalized Customer Purchase Health Engine
- Added standardized 0-100 Purchase Health Score
- Added Purchase Health Tier classification
- Completed QA validations

Author:
Mat Thompson

Created:
2026-08-07

Version:
1.0
============================================================
*/
-- ============================================================
-- Stage 1: Customer Purchase History
-- Collect a chronological history of successful customer
-- purchases to establish the foundation for behavioral analysis.
-- ============================================================
WITH CustomerPurchaseHistory AS
(
    SELECT
        c.CustomerID,
        o.OrderID,
        p.PaymentDateTime

    FROM
        customers AS c

    INNER JOIN orders AS o
        ON c.CustomerID = o.CustomerID

    INNER JOIN payments AS p
        ON o.OrderID = p.OrderID

    WHERE
        p.PaymentStatus = 'Successful'
),
-- ============================================================
-- Stage 2: Purchase Intervals
-- Identify each customer's previous purchase so the time
-- between consecutive purchases can be measured.
-- ============================================================
PurchaseIntervals AS
(
    SELECT
        cph.CustomerID,
        cph.OrderID,
        cph.PaymentDateTime,

        LAG(cph.PaymentDateTime) OVER
        (
            PARTITION BY cph.CustomerID
            ORDER BY cph.PaymentDateTime
        ) AS PreviousPurchaseDate

    FROM
        CustomerPurchaseHistory AS cph
),
-- ============================================================
-- Stage 3: Purchase Intervals with Days
-- Calculate the number of days between consecutive purchases
-- for every customer.
-- ============================================================
PurchaseIntervalsWithDays AS
(
    SELECT
        pi.CustomerID,
        pi.OrderID,
        pi.PaymentDateTime,
        pi.PreviousPurchaseDate,

        DATEDIFF
        (
            DAY,
            pi.PreviousPurchaseDate,
            pi.PaymentDateTime
        ) AS DaysBetweenPurchases

    FROM
        PurchaseIntervals AS pi
),
-- ============================================================
-- Stage 4: Historical Behavior Profile
-- Build a historical purchasing profile for each customer by
-- calculating their average purchase interval, most recent
-- purchase, purchase count, and customer type.
-- ============================================================
HistoricalBehaviorProfile AS
(
    SELECT
        pid.CustomerID,
        AVG(pid.DaysBetweenPurchases) AS AverageDaysBetweenPurchases,
        MAX(pid.PaymentDateTime) AS LastPurchaseDate,
        COUNT(pid.OrderID) AS SuccessfulOrderCount,

        CASE
            WHEN COUNT(pid.OrderID) = 1
                THEN 'One-Time Customer'
            ELSE
                'Repeat Customer'
        END AS CustomerType

    FROM
        PurchaseIntervalsWithDays AS pid

    GROUP BY
        pid.CustomerID
),
-- ============================================================
-- Stage 5: Current Purchase State
-- Measure each customer's current inactivity by calculating
-- the number of days since their last successful purchase.
-- ============================================================
CurrentPurchaseState AS
(
    SELECT
        hbp.CustomerID,
        hbp.AverageDaysBetweenPurchases,
        hbp.LastPurchaseDate,
        hbp.SuccessfulOrderCount,
        hbp.CustomerType,

        DATEDIFF
        (
            DAY,
            hbp.LastPurchaseDate,
            GETDATE()
        ) AS DaysSinceLastPurchase

    FROM
        HistoricalBehaviorProfile AS hbp
),
-- ============================================================
-- Stage 6: Purchase Deviation
-- Compare each customer's current inactivity against their
-- historical purchasing behavior.
-- ============================================================
PurchaseDeviation AS
(
    SELECT
        cps.CustomerID,
        cps.AverageDaysBetweenPurchases,
        cps.LastPurchaseDate,
        cps.SuccessfulOrderCount,
        cps.CustomerType,
        cps.DaysSinceLastPurchase,

        cps.DaysSinceLastPurchase
            - cps.AverageDaysBetweenPurchases
            AS DaysBeyondOrWithinAverage

    FROM
        CurrentPurchaseState AS cps
),
-- ============================================================
-- Stage 7: Healthy Window
-- Create a personalized healthy purchasing window by applying
-- a 20% grace period to each customer's average purchase
-- interval.
-- ============================================================
HealthyWindow AS
(
    SELECT
        pd.CustomerID,
        pd.AverageDaysBetweenPurchases,
        pd.LastPurchaseDate,
        pd.SuccessfulOrderCount,
        pd.CustomerType,
        pd.DaysSinceLastPurchase,
        pd.DaysBeyondOrWithinAverage,

        pd.AverageDaysBetweenPurchases
            * 0.2
            AS GracePeriodDays,

        pd.AverageDaysBetweenPurchases
            + (pd.AverageDaysBetweenPurchases * 0.2)
            AS HealthyWindowDays

    FROM
        PurchaseDeviation AS pd
),
-- ============================================================
-- Stage 8: Percent Deviation
-- Measure how far a customer has moved beyond their healthy
-- purchasing window and convert that deviation into a
-- standardized percentage.
-- ============================================================
PercentDeviation AS
(
    SELECT
        hw.CustomerID,
        hw.AverageDaysBetweenPurchases,
        hw.LastPurchaseDate,
        hw.SuccessfulOrderCount,
        hw.CustomerType,
        hw.DaysSinceLastPurchase,
        hw.DaysBeyondOrWithinAverage,
        hw.GracePeriodDays,
        hw.HealthyWindowDays,

        CASE
            WHEN hw.DaysSinceLastPurchase <= hw.HealthyWindowDays
                THEN 0
            ELSE
                hw.DaysSinceLastPurchase - hw.HealthyWindowDays
        END AS DaysBeyondHealthyWindow,

        CASE
            WHEN hw.HealthyWindowDays IS NULL
                THEN NULL

            WHEN hw.HealthyWindowDays = 0
                THEN NULL

            WHEN hw.DaysSinceLastPurchase <= hw.HealthyWindowDays
                THEN 0

            ELSE
                (hw.DaysSinceLastPurchase - hw.HealthyWindowDays)
                / NULLIF(hw.HealthyWindowDays, 0)
        END AS PercentBeyondHealthyWindow

    FROM
        HealthyWindow AS hw
),
-- ============================================================
-- Stage 9: Health Score Calculation
-- Convert percentage deviation into a standardized
-- Purchase Health Score ranging from 0 to 100.
-- ============================================================
HealthScoreCalculation AS
(
    SELECT
        pd.CustomerID,
        pd.AverageDaysBetweenPurchases,
        pd.LastPurchaseDate,
        pd.SuccessfulOrderCount,
        pd.CustomerType,
        pd.DaysSinceLastPurchase,
        pd.DaysBeyondOrWithinAverage,
        pd.GracePeriodDays,
        pd.HealthyWindowDays,
        pd.DaysBeyondHealthyWindow,
        pd.PercentBeyondHealthyWindow,

        CASE
            WHEN pd.PercentBeyondHealthyWindow IS NULL
                THEN NULL

            WHEN pd.PercentBeyondHealthyWindow >= 1
                THEN 0

            ELSE
                100 - (pd.PercentBeyondHealthyWindow * 100)
        END AS PurchaseHealthScore

    FROM
        PercentDeviation AS pd
),
-- ============================================================
-- Stage 10: Purchase Health Tier
-- Translate the numerical Purchase Health Score into
-- business-friendly health classifications.
-- ============================================================
PurchaseHealthTier AS
(
    SELECT
        hsc.CustomerID,
        hsc.AverageDaysBetweenPurchases,
        hsc.LastPurchaseDate,
        hsc.SuccessfulOrderCount,
        hsc.CustomerType,
        hsc.DaysSinceLastPurchase,
        hsc.DaysBeyondOrWithinAverage,
        hsc.GracePeriodDays,
        hsc.HealthyWindowDays,
        hsc.DaysBeyondHealthyWindow,
        hsc.PercentBeyondHealthyWindow,
        hsc.PurchaseHealthScore,

        CASE
            WHEN hsc.PurchaseHealthScore IS NULL
                THEN 'Insufficient History'

            WHEN hsc.PurchaseHealthScore >= 95
                THEN 'Healthy'

            WHEN hsc.PurchaseHealthScore >= 80
                THEN 'Watch'

            WHEN hsc.PurchaseHealthScore >= 60
                THEN 'At Risk'

            ELSE
                'Critical'
        END AS PurchaseHealthTier

    FROM
        HealthScoreCalculation AS hsc
)

SELECT
    *
FROM
    PurchaseHealthTier;

/*

/*TIER DISTRIBUTION QA*/
SELECT
    pht.PurchaseHealthTier,
    COUNT(*) AS CustomerCount

FROM
    PurchaseHealthTier AS pht

GROUP BY 
	pht.PurchaseHealthTier
	
ORDER BY
    CASE
		WHEN PurchaseHealthTier = 'Healthy' THEN 1
		WHEN PurchaseHealthTier = 'Watch' THEN 2
		WHEN PurchaseHealthTier = 'At Risk' THEN 3
        WHEN PurchaseHealthTier = 'Critical' THEN 4
        WHEN PurchaseHealthTier = 'Insufficient History' THEN 5
    END;

/*SCORE RANGE QA*/
SELECT
	MIN(pht.PurchaseHealthScore) AS MinHealthScore,
	MAX(pht.PurchaseHealthScore) AS MaxHealthScore

FROM
	PurchaseHealthTier AS pht;




/*HEALTHY CUSTOMERS LOOK HEALTHY QA*/
SELECT TOP (20)
    pht.CustomerID,
    pht.AverageDaysBetweenPurchases,
    pht.DaysSinceLastPurchase,
    pht.HealthyWindowDays,
    pht.PurchaseHealthScore,
    pht.PurchaseHealthTier
FROM
    PurchaseHealthTier AS pht
ORDER BY
    pht.PurchaseHealthScore DESC;




/*CRITICAL CUSTOMERS DESERVE ATTENTION QA*/
SELECT TOP (20)
    pht.CustomerID,
    pht.AverageDaysBetweenPurchases,
    pht.DaysSinceLastPurchase,
    pht.HealthyWindowDays,
    pht.DaysBeyondHealthyWindow,
    pht.PercentBeyondHealthyWindow,
    pht.PurchaseHealthScore,
    pht.PurchaseHealthTier
FROM
    PurchaseHealthTier AS pht
WHERE
	pht.PurchaseHealthScore IS NOT NULL
ORDER BY
    pht.PurchaseHealthScore ASC;


*/

