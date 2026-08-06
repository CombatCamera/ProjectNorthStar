


/*
============================================================
NorthStar Commerce

File:
02_revenue_by_category.sql

Purpose:
Calculates product-line revenue by category for orders
with a successful payment.

Business Question:
Which product categories generate the most revenue?

Metric Definition:
Category Revenue = SUM(order_items.LineTotal)
for orders where PaymentStatus = 'Successful'.

Author:
Mat Thompson

Created:
2026-08-03

Version:
1.0
============================================================
*/

SELECT
	c.CategoryName,
	SUM(oi.LineTotal) AS CategoryRevenue
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
    CategoryRevenue DESC;