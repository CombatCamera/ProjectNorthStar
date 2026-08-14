"""
===============================================================================
Project:        Project NorthStar
Engine:         Privacy Engine
File:           privacy_engine.py
Author:         Mat Thompson
Created:        2026-08-13
Version:        1.0

Purpose:
    Protect customer privacy by generating anonymized datasets while preserving
    the business relationships required for downstream analytics and machine
    learning.

Inputs:
    - customers.csv
    - orders.csv
    - payments.csv

Outputs:
    - anonymous_customers.csv
    - anonymous_orders.csv
    - anonymous_payments.csv

Responsibilities:
    - Generate dataset-scoped AnonymousCustomerKey values.
    - Replace CustomerID with AnonymousCustomerKey.
    - Remove unnecessary personally identifiable information (PII).
    - Preserve relationships across all processed tables.

Non-Responsibilities:
    - Feature engineering
    - Purchase Health calculations
    - Machine learning
    - Predictive analytics
    - Revenue analysis
    - Category-aware purchasing analysis

Engineering Laws:
    1. Every field must earn its place.
    2. Every engine has one responsibility.
    3. No useful idea is discarded.

===============================================================================
"""

import uuid
import csv
import os

# =============================================================================
# Configuration
# =============================================================================
customer_file = os.getenv("NORTHSTAR_CUSTOMER_FILE")
order_file = os.getenv("NORTHSTAR_ORDER_FILE")
payment_file = os.getenv("NORTHSTAR_PAYMENT_FILE")


CUSTOMER_OUTPUT_FILE = "data/privacy_filtered/anonymous_customers.csv"

ORDER_OUTPUT_FILE = "data/privacy_filtered/anonymous_orders.csv"

PAYMENT_OUTPUT_FILE = "data/privacy_filtered/anonymous_payments.csv"

PURCHASE_HISTORY_OUTPUT_FILE = "data/privacy_filtered/anonymous_purchase_history.csv"





# Customer Whitelist
CUSTOMER_OUTPUT_FIELDS = [
    "AnonymousCustomerKey",
    "JoinDate",
]

# Orders Whitelist
ORDER_OUTPUT_FIELDS = [
    "AnonymousOrderKey",
    "AnonymousCustomerKey",
    "OrderDateTime",
]
# Payments Whitelist 
PAYMENT_OUTPUT_FIELDS = [
    "AnonymousOrderKey",
    "PaymentAttempt",
    "PaymentDateTime",
    "PaymentStatus",
]

#Purchase history output
PURCHASE_HISTORY_OUTPUT_FIELDS = [
    "AnonymousCustomerKey",
    "JoinDate",
    "AnonymousOrderKey",
    "OrderDateTime",
    "PaymentAttempt",
    "PaymentDateTime",
    "PaymentStatus",
]

# =============================================================================
# Helper Functions
# =============================================================================
# Loading
def load_csv(file_path):
    data = []
    
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            data.append(row)

    return data

# CUSTOMER MAPPING
def generate_anonymous_customer_mapping(customer_data):
    
    anonymous_customer_map = {}
        
    for customer in customer_data:
        customer_id = customer["CustomerID"]
        anonymous_customer_key = str(uuid.uuid4())
        anonymous_customer_map[customer_id] = anonymous_customer_key
        
    return anonymous_customer_map

# ORDER MAPPING
def generate_anonymous_order_mapping(order_data):
    
    anonymous_order_map = {}
    
    for order in order_data:
        order_id = order["OrderID"]
        anonymous_order_key = str(uuid.uuid4())
        anonymous_order_map[order_id] = anonymous_order_key
        
    return anonymous_order_map

# CUSTOMER
def filter_customer_data(customer_data, anonymous_customer_map):
    
    privacy_filtered_customer_data = []

    for customer in customer_data:
        customer_id = customer["CustomerID"]
        anonymous_customer_key = anonymous_customer_map[customer_id]
        privacy_filtered_customer = {
            "AnonymousCustomerKey": anonymous_customer_key,
            "JoinDate": customer["JoinDate"]
        }
        privacy_filtered_customer_data.append(privacy_filtered_customer)
    
    return privacy_filtered_customer_data


# ORDERS
def filter_order_data(order_data, anonymous_customer_map, anonymous_order_map):
    
    privacy_filtered_order_data = []

    for order in order_data:
        order_id = order["OrderID"]
        customer_id = order["CustomerID"]
        anonymous_customer_key = anonymous_customer_map[customer_id]
        anonymous_order_key = anonymous_order_map[order_id]
        privacy_filtered_order = {
            "AnonymousOrderKey": anonymous_order_key,
            "AnonymousCustomerKey": anonymous_customer_key,
            "OrderDateTime": order["OrderDateTime"]
        }
        privacy_filtered_order_data.append(privacy_filtered_order)
    
    return privacy_filtered_order_data


# PAYMENTS
def filter_payment_data(payment_data, anonymous_order_map):
    
    privacy_filtered_payment_data = []
    
    for payment in payment_data:
        order_id = payment["OrderID"]
        anonymous_order_key = anonymous_order_map[order_id]
        payment_attempt = payment["PaymentAttempt"]
        payment_status = payment["PaymentStatus"]
        privacy_filtered_payment = {
            "AnonymousOrderKey": anonymous_order_key,
            "PaymentAttempt": payment_attempt,
            "PaymentDateTime": payment["PaymentDateTime"],
            "PaymentStatus": payment_status
        }
        privacy_filtered_payment_data.append(privacy_filtered_payment)
        
    return privacy_filtered_payment_data

# MERGE ANONYMOUS DATA
def reconstruct_purchase_history(privacy_filtered_customer_data, privacy_filtered_order_data, privacy_filtered_payment_data):

    anonymous_purchase_history_data = []
    
    customer_lookup = {}
    order_lookup = {}
    
    
    for customer in privacy_filtered_customer_data:
        anonymous_customer_key = customer["AnonymousCustomerKey"]
        customer_lookup[anonymous_customer_key] = customer
    
    
    for order in privacy_filtered_order_data:
        anonymous_order_key = order["AnonymousOrderKey"]
        order_lookup[anonymous_order_key] = order
        
        
    for payment in privacy_filtered_payment_data:
        anonymous_order_key = payment["AnonymousOrderKey"]
        
        order = order_lookup[anonymous_order_key]
        
        anonymous_customer_key = order["AnonymousCustomerKey"]
        
        customer = customer_lookup[anonymous_customer_key]
       
        payment_history = {
            "AnonymousCustomerKey": anonymous_customer_key,
            "JoinDate": customer["JoinDate"],
            "AnonymousOrderKey": anonymous_order_key,
            "OrderDateTime": order["OrderDateTime"],
            "PaymentAttempt": payment["PaymentAttempt"],
            "PaymentDateTime": payment["PaymentDateTime"],
            "PaymentStatus": payment["PaymentStatus"]
         }
            
        anonymous_purchase_history_data.append(payment_history)
    
    return anonymous_purchase_history_data


def write_csv(file_path, data, fieldnames):
    
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

# =============================================================================
# Main Function
# =============================================================================

def main(customer_file, order_file, payment_file):
    
    #Validate required environment variables
    if customer_file is None:
        raise RuntimeError(
            "Missing required environment variable: NORTHSTAR_CUSTOMER_FILE"
        )
        
    if order_file is None:
        raise RuntimeError(
            "Missing required environment variable: NORTHSTAR_ORDER_FILE"
        )
        
    if payment_file is None:
        raise RuntimeError(
            "Missing required environment variable: NORTHSTAR_PAYMENT_FILE"
        )
    
    # Load customers
    customer_data = load_csv(customer_file)
    
    # Load orders
    order_data = load_csv(order_file)
    
    # Load payments
    payment_data = load_csv(payment_file)
    
    
    # Generate anonymous mapping
    anonymous_customer_map = generate_anonymous_customer_mapping(customer_data)
    anonymous_order_map = generate_anonymous_order_mapping(order_data)
    
    
    # Filter customer data
    privacy_filtered_customer_data = filter_customer_data(
        customer_data,
        anonymous_customer_map
    )
    
    # Filter order data
    privacy_filtered_order_data = filter_order_data(
        order_data,
        anonymous_customer_map,
        anonymous_order_map
    )
    
    # Filter payment data
    privacy_filtered_payment_data = filter_payment_data(
        payment_data,
        anonymous_order_map
    )
    
    # Reconstruct purchase history
    anonymous_purchase_history_data = reconstruct_purchase_history(
        privacy_filtered_customer_data,
        privacy_filtered_order_data,
        privacy_filtered_payment_data
    )
 
     
    # QA Validation
    
    
    # Save anonumized datasets
    write_csv(
        CUSTOMER_OUTPUT_FILE,
        privacy_filtered_customer_data,
        CUSTOMER_OUTPUT_FIELDS
    )
    
    write_csv(
        ORDER_OUTPUT_FILE,
        privacy_filtered_order_data,
        ORDER_OUTPUT_FIELDS
    )
    
    write_csv(
        PAYMENT_OUTPUT_FILE,
        privacy_filtered_payment_data,
        PAYMENT_OUTPUT_FIELDS
    )
    
    write_csv(
        PURCHASE_HISTORY_OUTPUT_FILE,
        anonymous_purchase_history_data,
        PURCHASE_HISTORY_OUTPUT_FIELDS
    )
    
    
if __name__ == "__main__":
    main(customer_file, order_file, payment_file)