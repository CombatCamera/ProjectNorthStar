/*
============================================================
NorthStar Commerce

File:
13_customer_last_purchase_date.sql

Purpose:
Reports the most recent successful purchase date for
each customer.

Business Question:
When did each customer last make a successful purchase?

Metric Definition:
Last Purchase Date =
MAX(payments.PaymentDateTime)

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
	c.CustomerID,
	c.FirstName,
	c.LastName,
	MAX(p.PaymentDateTime) AS LastPurchaseDate
	
FROM
	payments AS p

INNER JOIN orders AS o
	ON (p.OrderID = o.OrderID)

INNER JOIN customers AS c
	ON (o.CustomerID = c.CustomerID)

WHERE
	p.PaymentStatus = 'Successful'

GROUP BY
	c.CustomerID,
	c.FirstName,
	c.LastName

ORDER BY
	LastPurchaseDate ASC;



	