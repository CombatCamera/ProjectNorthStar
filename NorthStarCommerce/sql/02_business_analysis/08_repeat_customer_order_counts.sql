/*
============================================================
NorthStar Commerce

File:
08_repeat_customer_order_counts.sql

Purpose:
Identifies customers who have placed more than one
successfully paid order and reports their total number
of successful orders.

Business Question:
Which customers are repeat customers?

Metric Definition:
Repeat Customer =
A customer with more than one successfully paid order.

Successful Order Count =
COUNT(orders.OrderID)

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
    o.CustomerID,
    c.FirstName,
    c.LastName,
    COUNT(o.OrderID) AS SuccessfulOrderCount
FROM
	payments AS p
INNER JOIN
	orders AS o
ON 
	p.OrderID = o.OrderID
INNER JOIN 
	customers AS c
ON 
	o.CustomerID = c.CustomerID
WHERE
	p.PaymentStatus = 'Successful'
GROUP BY
	o.CustomerID,
	c.FirstName,
	c.LastName
HAVING
	COUNT(o.OrderID) > 1
ORDER BY
	SuccessfulOrderCount DESC;
