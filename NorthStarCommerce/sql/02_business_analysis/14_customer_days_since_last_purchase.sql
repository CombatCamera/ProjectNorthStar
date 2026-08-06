/*
============================================================
NorthStar Commerce

File:
14_customer_days_since_last_purchase.sql

Purpose:
Calculates the number of days since each customer's most
recent successful purchase.

Business Question:
How long has it been since each customer last made a
successful purchase?

Metric Definition:
Last Purchase Date =
MAX(payments.PaymentDateTime)

Days Since Last Purchase =
DATEDIFF(
    DAY,
    LastPurchaseDate,
    GETDATE()
)

Includes only orders where
PaymentStatus = 'Successful'.

Author:
Mat Thompson

Created:
2026-08-05

Version:
1.0
============================================================
*/
;WITH CustomerLastPurchase AS
(
    SELECT
        c.CustomerID,
        c.FirstName,
        c.LastName,
        MAX(p.PaymentDateTime) AS LastPurchaseDate
    FROM
        payments AS p

    INNER JOIN orders AS o
        ON p.OrderID = o.OrderID

    INNER JOIN customers AS c
        ON o.CustomerID = c.CustomerID

    WHERE
        p.PaymentStatus = 'Successful'

    GROUP BY
        c.CustomerID,
        c.FirstName,
        c.LastName
)

SELECT
    CustomerID,
    FirstName,
    LastName,
    LastPurchaseDate,
    DATEDIFF(
        DAY,
        LastPurchaseDate,
        GETDATE()
    ) AS DaysSinceLastPurchase
FROM
    CustomerLastPurchase
ORDER BY
    DaysSinceLastPurchase DESC;