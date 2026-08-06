/*
============================================================
NorthStar Commerce

File:
09_top_10_products_by_units_sold.sql

Purpose:
Identifies the ten products with the highest number of
units sold from successfully paid orders.

Business Question:
Which products sell the most units?

Metric Definition:
Units Sold =
SUM(order_items.Quantity)

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
	SUM(oi.Quantity) AS UnitsSold
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
WHERE
	p.PaymentStatus = 'Successful'
GROUP BY
	pr.ProductID,
	pr.ProductName
ORDER BY
	UnitsSold DESC;