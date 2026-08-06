/*
============================================================
NorthStar Commerce

File:
11_top_10_products_by_gross_profit.sql

Purpose:
Identifies the ten products that generated the highest
gross profit from successfully paid orders.

Business Question:
Which products generate the most gross profit?

Metric Definition:
Gross Profit =
SUM(
    order_items.LineTotal
    -
    (products.UnitCost * order_items.Quantity)
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

SELECT
    TOP (10)
    pr.ProductID,
    pr.ProductName,
    SUM(oi.LineTotal - (pr.UnitCost * oi.Quantity)) AS GrossProfit

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
    GrossProfit DESC;
