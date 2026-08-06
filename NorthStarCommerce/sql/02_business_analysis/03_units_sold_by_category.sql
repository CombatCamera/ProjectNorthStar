/*
============================================================
NorthStar Commerce

File:
03_units_sold_by_category.sql

Purpose:
Calculates the total number of product units sold in each
category for orders with a successful payment.

Business Question:
Which product categories sell the most units?

Metric Definition:
Units Sold = SUM(order_items.Quantity)
for orders where PaymentStatus = 'Successful'.

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
INNER JOIN
	categories AS c
ON
	pr.CategoryID = c.CategoryID
WHERE
	p.PaymentStatus = 'Successful'
GROUP BY
	c.CategoryName
ORDER BY
	UnitsSold DESC;

	