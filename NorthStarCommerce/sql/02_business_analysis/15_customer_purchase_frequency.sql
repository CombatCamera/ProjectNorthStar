/*
============================================================
NorthStar Commerce

File:
15_customer_purchase_frequency.sql

Purpose:
Calculates each customer's purchasing activity by counting
successful orders and returning the customer's first
purchase date, last purchase date, and active lifetime.

Business Question:
How many successful orders has each customer placed, and
over what period of time have they been an active customer?

Metric Definition:
Successful Orders =
COUNT(DISTINCT orders.OrderID)

First Purchase Date =
MIN(payments.PaymentDateTime)

Last Purchase Date =
MAX(payments.PaymentDateTime)

Active Customer Days =
DATEDIFF(
    DAY,
    FirstPurchaseDate,
    LastPurchaseDate
)

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

SELECT
    c.CustomerID,
    CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName,
    COUNT(DISTINCT o.OrderID) AS SuccessfulOrders,
    MIN(p.PaymentDateTime) AS FirstPurchase,
    MAX(p.PaymentDateTime) AS LastPurchase,
    DATEDIFF(
        DAY,
        MIN(p.PaymentDateTime),
        MAX(p.PaymentDateTime)
    ) AS ActiveCustomerDays
FROM dbo.customers AS c
INNER JOIN dbo.orders AS o
    ON c.CustomerID = o.CustomerID
INNER JOIN dbo.payments AS p
    ON o.OrderID = p.OrderID
WHERE p.PaymentStatus = 'Successful'
GROUP BY
    c.CustomerID,
    c.FirstName,
    c.LastName
ORDER BY
    SuccessfulOrders DESC;
