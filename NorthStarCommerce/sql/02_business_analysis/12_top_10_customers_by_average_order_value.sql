/*
============================================================
NorthStar Commerce

File:
12_top_10_customers_by_average_order_value.sql

Purpose:
Identifies the ten customers with the highest average
order value from successfully paid orders.

Business Question:
Which customers spend the most on average per order?

Metric Definition:
Average Order Value =
SUM(payments.PaymentAmount)
/
COUNT(DISTINCT payments.OrderID)

Calculated separately for each customer.

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

SELECT TOP (10)
    c.CustomerID,
    c.FirstName,
    c.LastName,
    CAST(
        SUM(p.PaymentAmount)
        / COUNT(DISTINCT p.OrderID)
        AS DECIMAL(10,2)
    ) AS AverageOrderValue
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

ORDER BY
    AverageOrderValue DESC;



	