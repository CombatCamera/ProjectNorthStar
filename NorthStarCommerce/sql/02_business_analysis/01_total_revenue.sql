/*
============================================================
NorthStar Commerce

File:
01_total_revenue.sql

Purpose:
Calculates the total revenue successfully collected
by NorthStar Commerce.

Business Question:
How much revenue has the company actually collected?

Metric Definition:
Total Revenue = SUM(payments.PaymentAmount)
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
    SUM(PaymentAmount) AS TotalRevenue
FROM
    payments
WHERE
    PaymentStatus = 'Successful';
    