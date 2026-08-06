/*
============================================================
NorthStar Commerce

File:
10_top_10_products_by_revenue.sql

Purpose:
Identifies the ten products that have generated the
highest total revenue from successfully paid orders.

Business Question:
Which products generate the most revenue?

Metric Definition:
Product Revenue =
SUM(order_items.LineTotal)

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
    pr.ProductID,
    pr.ProductName,
    SUM(oi.LineTotal) AS ProductRevenue
FROM
    payments AS p

INNER JOIN orders AS o
    ON p.OrderID = o.OrderID

INNER JOIN order_items AS oi
    ON o.OrderID = oi.OrderID

INNER JOIN products AS pr
    ON oi.ProductID = pr.ProductID

WHERE
    p.PaymentStatus = 'Successful'

GROUP BY
    pr.ProductID,
    pr.ProductName

ORDER BY
    ProductRevenue DESC;




