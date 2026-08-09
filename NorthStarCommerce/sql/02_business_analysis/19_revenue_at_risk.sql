/*
============================================================
NorthStar Commerce

File:
19_revenue_at_risk.sql

Purpose:
Measures the amount of historical revenue associated
with each Customer Purchase Health Tier to quantify
the potential business impact of customer retention.

Business Question:
How much successful payment revenue is associated
with each Purchase Health Tier, and how many
customers belong to each group?

Business Context:
The Customer Purchase Health Engine identifies which
customers appear Healthy, Watch, At Risk, or Critical
based on their purchasing behavior.

This report extends that analysis by measuring the
historical revenue represented by each health tier,
allowing business leaders to prioritize customer
retention efforts based on financial impact rather
than customer counts alone.

Revenue is calculated using successful payments only,
ensuring all reported values represent realized revenue.

Metrics Used:
- Purchase Health Tier
- Customer Count
- Lifetime Revenue

Expected Output:
One row per Purchase Health Tier including:
- Purchase Health Tier
- Customer Count
- Lifetime Revenue

Business Value:
This report helps NorthStar answer questions such as:
- How much revenue is represented by Critical customers?
- Which customer segments present the greatest
  retention opportunity?
- Where should customer retention resources be focused?

Model Notes:
- Revenue is based on successful payments only.
- Customer counts represent unique customers.
- Lifetime Revenue represents the sum of all successful
  payments for customers within each Purchase Health Tier.

Author:
Mat Thompson

Created:
2026-08-08

Version:
1.0
============================================================
*/

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
-- ============================================================
-- Stage 11: Revenue at Risk
-- Join the Customer Purchase Health Engine to customer
-- orders and successful payments to measure the historical
-- revenue represented by each Purchase Health Tier.
-- ============================================================
SELECT
    pht.PurchaseHealthTier,
    COUNT(DISTINCT pht.CustomerID) AS CustomerCount,
    CAST(
        SUM(p.PaymentAmount) 
        AS DECIMAL(18,2)
    ) AS LifetimeRevenue
FROM
    PurchaseHealthTier AS pht

INNER JOIN orders AS o
    ON pht.CustomerID = o.CustomerID

INNER JOIN payments as p
    ON o.OrderID = p.OrderID

WHERE
    p.PaymentStatus = 'Successful'

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

