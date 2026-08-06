/*
============================================================
NorthStar Commerce

File:
07_average_order_value.sql

Purpose:
Calculates the average revenue collected per successfully
paid order.

Business Question:
What is the average order value?

Metric Definition:
Average Order Value =
SUM(payments.PaymentAmount)
/
COUNT(DISTINCT payments.OrderID)

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
    CAST(
        SUM(p.PaymentAmount)
        / COUNT(DISTINCT p.OrderID)
        AS DECIMAL(10,2)
    ) AS AverageOrderValue
FROM
    payments AS p
WHERE
    p.PaymentStatus = 'Successful';