/*
============================================================
NorthStar Commerce

File:
16_average_days_between_purchases.sql

Purpose:
Calculates the average number of days between each customer's
successful purchases.

Business Question:
On average, how many days pass between each customer's
successful purchases?

Metric Definition:
Days Between Purchases =
DATEDIFF(
    DAY,
    PreviousPurchaseDate,
    PaymentDateTime
)

Average Days Between Purchases =
AVG(DaysBetweenPurchases)

Includes only orders where
PaymentStatus = 'Successful'.

Author:
Mat Thompson

Created:
2026-08-06

Version:
1.0
============================================================
*/

WITH CustomerPurchases AS
(
    SELECT
        c.CustomerID,
        c.FirstName,
        c.LastName,
        o.OrderID,
        p.PaymentDateTime,

        LAG(p.PaymentDateTime) OVER
        (
            PARTITION BY c.CustomerID
            ORDER BY p.PaymentDateTime
        ) AS PreviousPurchaseDate

    FROM customers AS c

    INNER JOIN orders AS o
        ON c.CustomerID = o.CustomerID

    INNER JOIN payments AS p
        ON o.OrderID = p.OrderID

    WHERE p.PaymentStatus = 'Successful'
)

SELECT
    CustomerID,
    CONCAT(FirstName, ' ', LastName) AS CustomerName,

    CAST(
        AVG(
            CAST(DaysBetweenPurchases AS DECIMAL(10,2))
        ) AS DECIMAL(10,2)
    ) AS AverageDaysBetweenPurchases

FROM
(
    SELECT
        CustomerID,
        FirstName,
        LastName,

        DATEDIFF
        (
            DAY,
            PreviousPurchaseDate,
            PaymentDateTime
        ) AS DaysBetweenPurchases

    FROM CustomerPurchases

    WHERE PreviousPurchaseDate IS NOT NULL

) AS PurchaseIntervals

GROUP BY
    CustomerID,
    FirstName,
    LastName

ORDER BY
    AverageDaysBetweenPurchases ASC;