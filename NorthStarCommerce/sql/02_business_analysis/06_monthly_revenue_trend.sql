
/*
============================================================
NorthStar Commerce

File:
06_monthly_revenue_trend.sql

Purpose:
Calculates monthly revenue from successfully paid orders
to identify revenue trends over time.

Business Question:
How has monthly revenue changed over time?

Metric Definition:
Monthly Revenue =
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
	YEAR(p.PaymentDateTime) AS RevenueYear, 
	MONTH(p.PaymentDateTime) AS RevenueMonth,
	SUM(p.PaymentAmount) AS MonthlyRevenue
FROM
	payments AS p
WHERE
	p.PaymentStatus = 'Successful'
GROUP BY
	YEAR(p.PaymentDateTime), 
	MONTH(p.PaymentDateTime)
ORDER BY
	RevenueYear, RevenueMonth;