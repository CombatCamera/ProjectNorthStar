
/*
============================================================
NorthStar Commerce

File:
04_average_selling_price_by_category.sql

Purpose:
Calculates the average selling price per unit for each product category based on 
successfully paid orders.

Business Question:
Which product categories have the highest average selling price per unit?

Metric Definition:

    Average Selling Price Per Unit =
    SUM(order_items.LineTotal)
    /
    SUM(order_items.Quantity)

    Includes only orders where
    PaymentStatus = 'Successful'.

Author:
Mat Thompson

Created:
2026-08-04

Version:
1.0
============================================================
*/

SELECT
    c.CategoryName,
    CAST(
        SUM(oi.LineTotal)
        / CAST(SUM(oi.Quantity) AS DECIMAL(10,2))
        AS DECIMAL(10,2)
    ) AS AverageSellingPricePerUnit
FROM
    payments AS p

INNER JOIN
    orders AS o
ON
    p.OrderID = o.OrderID

INNER JOIN
    order_items AS oi
ON
    o.OrderID = oi.OrderID

INNER JOIN
    products AS pr
ON
    oi.ProductID = pr.ProductID

INNER JOIN
    categories AS c
ON
    pr.CategoryID = c.CategoryID

WHERE
    p.PaymentStatus = 'Successful'
GROUP BY
    c.CategoryName
ORDER BY
    AverageSellingPricePerUnit DESC;