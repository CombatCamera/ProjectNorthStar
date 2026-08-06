/*
============================================================
NorthStar Commerce

File:
05_top_10_customers_by_revenue.sql

Purpose:
Identifies the ten customers who have generated the highest
total revenue from successfully paid orders.

Business Question:
Who are the Top 10 customers by total revenue?

Metric Definition:
Customer Revenue =
SUM(payments.PaymentAmount)

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
	c.CustomerID,
	c.FirstName,
	c.LastName,
	SUM(p.PaymentAMount) AS CustomerREvenue
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
	c.CustomerID, 
	c.FirstName, 
	c.LastName
ORDER BY
	CustomerRevenue DESC;