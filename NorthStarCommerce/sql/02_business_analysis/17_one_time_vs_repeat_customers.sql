/*
============================================================
NorthStar Commerce

File:
17_one_time_vs_repeat_customers.sql

Purpose:
Classifies customers as either one-time or repeat customers
based on their number of successful orders.

Business Question:
How many customers purchased only once, and how many returned
to make additional successful purchases?

Metric Definition:
Successful Order Count =
COUNT(DISTINCT orders.OrderID)

Customer Type =
'One-Time Customer' when Successful Order Count = 1

'Repeat Customer' when Successful Order Count > 1

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
WITH CustomerOrderCounts AS
(
    SELECT
        c.CustomerID,
        COUNT(DISTINCT o.OrderID) AS SuccessfulOrders
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.CustomerID = o.CustomerID
    INNER JOIN payments AS p
        ON o.OrderID = p.OrderID
    WHERE p.PaymentStatus = 'Successful'
    GROUP BY
        c.CustomerID
),

CustomerClassifications AS
(
    SELECT
        CustomerID,
        SuccessfulOrders,
        CASE
            WHEN SuccessfulOrders = 1
                THEN 'One-Time Customer'
            ELSE
                'Repeat Customer'
        END AS CustomerType
    FROM CustomerOrderCounts
),

CustomerTotals AS 
(
    SELECT
        COUNT(CustomerID) AS TotalCustomers
    FROM CustomerOrderCounts
)

SELECT
    cc.CustomerType,
    COUNT(cc.CustomerID) AS CustomerCount,
    CAST(
        COUNT(cc.CustomerID) * 100.0 / ct.TotalCustomers
        AS DECIMAL(10, 2)
    ) AS PercentageOfCustomers
FROM CustomerClassifications AS cc
CROSS JOIN CustomerTotals AS ct
GROUP BY
    cc.CustomerType,
    ct.TotalCustomers;