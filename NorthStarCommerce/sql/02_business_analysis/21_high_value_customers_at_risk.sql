/*
============================================================
NorthStar Commerce

File:
21_high_value_customers_at_risk.sql

Purpose:
Identifies the highest-value customers currently
classified as At Risk or Critical by combining
Purchase Health metrics with Customer Lifetime
Revenue to create a prioritized customer retention
action list.

Business Question:
Which At Risk and Critical customers should
NorthStar prioritize for proactive retention
efforts based on both purchasing behavior and
historical customer value?

Business Context:
Previous reports established a Customer Purchase
Health model and measured both the total revenue
represented by each Purchase Health Tier and the
average Customer Lifetime Value (CLV) of those
customers.

This report combines those analytical models to
identify specific customers who represent the
greatest retention opportunity.

Rather than measuring historical performance,
this report supports operational decision-making
by identifying which customers should receive
immediate attention from Customer Success,
Sales, or Account Management teams.

Metrics Used:
- Purchase Health Tier
- Purchase Health Score
- Customer Lifetime Revenue
- Last Purchase Date
- Days Since Last Purchase
- Average Days Between Purchases
- Days Beyond Healthy Window

Expected Output:
One row per customer including:
- Customer ID
- Purchase Health Tier
- Purchase Health Score
- Customer Lifetime Revenue
- Last Purchase Date
- Days Since Last Purchase
- Average Days Between Purchases
- Days Beyond Healthy Window

Business Value:
This report helps NorthStar answer questions such as:
- Which high-value customers require immediate
  retention efforts?
- Which customers have deviated the furthest from
  their normal purchasing behavior?
- Which customer relationships represent the
  greatest opportunity to preserve future revenue?

Model Notes:
- Only customers classified as At Risk or Critical
  are included.
- Customer Lifetime Revenue is calculated using
  successful payments only.
- Results are prioritized by business-defined
  Purchase Health Tier followed by Customer
  Lifetime Revenue and Purchase Health Score.
- This report is intended as an operational
  retention action list rather than a historical
  performance report.

  Revision History:
------------------------------------------------------------
Version 1.0 (2026-08-09)
- Initial release
- Added high-value At Risk and Critical customer action list
- Added Customer Lifetime Revenue prioritization
- Added Days Beyond Healthy Window context
- Added QA validation for completeness, revenue accuracy,
  and Purchase Health Tier business rules

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
),
-- ============================================================
-- Stage 11: Customer Lifetime Revenue
-- Calculate the total lifetime revenue generated by each
-- customer using successful payments only.
-- ============================================================
CustomerLifetimeRevenue AS
(
   SELECT
        pht.CustomerID,
        pht.PurchaseHealthTier,
        SUM(p.PaymentAmount) AS CustomerLifetimeRevenue
    FROM
        PurchaseHealthTier AS pht
    INNER JOIN orders AS o
        ON pht.CustomerID = o.CustomerID
    INNER JOIN payments AS p
        ON o.OrderID = p.OrderID
    WHERE
        p.PaymentStatus = 'Successful'
    GROUP BY 
        pht.CustomerID,
        pht.PurchaseHealthTier
),
-- ============================================================
-- Stage 12: High-Value Customers At Risk
-- Identify customers currently classified as At Risk or
-- Critical and combine their Purchase Health metrics with
-- Customer Lifetime Revenue to create a prioritized
-- retention action list.
-- ============================================================
HighValueCustomersAtRisk AS
(
    SELECT
        pht.CustomerID,
        pht.PurchaseHealthTier,
        pht.PurchaseHealthScore,
        clr.CustomerLifetimeRevenue,
        pht.LastPurchaseDate,
        pht.DaysSinceLastPurchase,
        pht.AverageDaysBetweenPurchases,
        pht.DaysBeyondHealthyWindow

    FROM
        PurchaseHealthTier AS pht

    INNER JOIN CustomerLifetimeRevenue AS clr
        ON pht.CustomerID = clr.CustomerID

    WHERE  
        pht.PurchaseHealthTier IN ('Critical', 'At Risk')
)

SELECT
    *
FROM
    HighValueCustomersAtRisk
ORDER BY
    CASE
        WHEN PurchaseHealthTier = 'Critical' THEN 1
        WHEN PurchaseHealthTier = 'At Risk' THEN 2
    END,
    CustomerLifetimeRevenue DESC,
    PurchaseHealthScore ASC;
/*
-- QA #1
-- DID EVERY AT RISK / CRITICAL CUSTOMER MAKE IT IN?
EngineCounts AS
(
    SELECT
        pht.PurchaseHealthTier,
        COUNT(DISTINCT pht.CustomerID) AS EngineCount

    FROM
        PurchaseHealthTier AS pht

    WHERE
        pht.PurchaseHealthTier IN ('Critical', 'At Risk')

    GROUP BY
        pht.PurchaseHealthTier

    
),

ReportCounts AS
(
    SELECT
        hvcr.PurchaseHealthTier,
        COUNT(DISTINCT hvcr.CustomerID) AS ReportCount
    FROM   
        HighValueCustomersAtRisk AS hvcr

    GROUP BY 
        hvcr.PurchaseHealthTier

)

SELECT
    ec.PurchaseHealthTier,
    ec.EngineCount,
    rc.ReportCount,

    CASE
        WHEN ec.EngineCount = rc.ReportCount
            THEN 'PASS'
        ELSE
            'FAIL'
    END AS QAStatus

FROM
    EngineCounts AS ec

INNER JOIN ReportCounts AS rc
    ON ec.PurchaseHealthTier = rc.PurchaseHealthTier

ORDER BY
    CASE
        WHEN ec.PurchaseHealthTier = 'Critical' THEN 1
        WHEN ec.PurchaseHealthTier = 'At Risk' THEN 2
    END;


-- QA #2
-- DID EACH CUSTOMER BRING THE CORRECT LIFETIME REVENUE WITH THEM?
SourceLifetimeRevenue AS
(
    SELECT
        clr.CustomerID,
        clr.CustomerLifetimeRevenue AS SourceLifetimeRevenue
    FROM
        CustomerLifetimeRevenue AS clr
),

ReportLifetimeRevenue AS
(
    SELECT
        hvcr.CustomerID,
        hvcr.CustomerLifetimeRevenue AS ReportLifetimeRevenue
    FROM
        HighValueCustomersAtRisk AS hvcr
)

SELECT
    slr.CustomerID,
    slr.SourceLifetimeRevenue,
    rlr.ReportLifetimeRevenue,

    CASE
        WHEN slr.SourceLifetimeRevenue = rlr.ReportLifetimeRevenue
            THEN 'PASS'
        ELSE
            'FAIL'
    END AS QAStatus

FROM
    SourceLifetimeRevenue AS slr

INNER JOIN ReportLifetimeRevenue AS rlr
    ON slr.CustomerID = rlr.CustomerID;

-- QA #3
-- Does every customer's Purchase Health Score correspond to the correct Purchase Health Tier?

ActualPurchaseHealthTier AS
(
    SELECT
        pht.CustomerID,
        pht.PurchaseHealthScore,
        pht.PurchaseHealthTier AS ActualPurchaseHealthTier

    FROM
        PurchaseHealthTier AS pht

    WHERE
        pht.PurchaseHealthTier IN ('Critical', 'At Risk')
),

ExpectedPurchaseHealthTier AS
(
    SELECT
        pht.CustomerID,
        pht.PurchaseHealthScore,

        CASE
            WHEN pht.PurchaseHealthScore >= 60
                THEN 'At Risk'
            ELSE
                'Critical'
        END AS ExpectedPurchaseHealthTier

    FROM
        PurchaseHealthTier AS pht

    WHERE
        pht.PurchaseHealthTier IN ('Critical', 'At Risk')
)

SELECT
    apht.CustomerID,
    apht.ActualPurchaseHealthTier,
    epht.ExpectedPurchaseHealthTier,

    CASE
        WHEN apht.ActualPurchaseHealthTier = epht.ExpectedPurchaseHealthTier
            THEN 'PASS'
        ELSE
            'FAIL'
    END AS QAStatus

FROM
    ActualPurchaseHealthTier AS apht

INNER JOIN ExpectedPurchaseHealthTier AS epht
    ON apht.CustomerID = epht.CustomerID;
*/