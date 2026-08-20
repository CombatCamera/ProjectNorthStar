'''
===============================================================================
Project:        Project NorthStar
Engine:         Privacy Engine
File:           privacy_engine.py
Author:         Mat Thompson
Created:        2026-08-13
Last Updated:   2026-08-18
Version:        2.1

Purpose:
    Transform QA-certified enterprise datasets into privacy-preserving
    analytical datasets suitable for external sharing while maintaining the
    business relationships required for downstream analytics, machine learning,
    and predictive modeling.

Inputs:
    - QA-certified NorthStar datasets
    - Dataset configuration
    - Environment variable file locations

Outputs:
    - Privacy-preserving datasets
    - Anonymous analytical datasets

Current Privacy Transformations:
    - Customer anonymization (UUID mapping)
    - Order anonymization (UUID mapping)
    - Customer-scoped temporal offset mapping
    - PII removal using field whitelists
    - Relationship reconstruction
    - Configurable dataset selection

Planned Privacy Transformations:
    - Configurable privacy modes
    - Optional intermediate datasets
    - Additional privacy-preserving transformations
    - Privacy QA certification

Responsibilities:
    - Process any QA-certified NorthStar dataset.
    - Generate dataset-scoped anonymous identifiers.
    - Apply customer-scoped temporal offsets.
    - Remove personally identifiable information (PII).
    - Preserve business relationships across datasets.
    - Produce privacy-safe datasets for external use.

Non-Responsibilities:
    - Data standardization
    - Business analytics
    - Feature engineering
    - Purchase Health calculations
    - Machine learning
    - Predictive analytics
    - Revenue analysis
    - Data quality validation

Engineering Laws:
    1. Every field must earn its place.
    2. Every engine has one responsibility.
    3. No useful idea is discarded.
    4. Every transformation leaves no trace.

Architecture:

                 QA Certified Data
                       │
           ┌───────────┴───────────┐
           │                       │
           ▼                       ▼
    Internal Processing      Privacy Engine
           │                       │
           ▼                       ▼
 Feature Engineering      Privacy-Safe Exports
 Machine Learning         Portfolio
 Analytics                Research
                           External Sharing

===============================================================================
'''
import uuid
import csv
import os
import random

from datetime import datetime, timedelta

# =============================================================================
# DATASET TO PROCESS
# =============================================================================

# DATASET = "operational"
DATASET = "training"

# =============================================================================
# Configuration
# =============================================================================



CUSTOMER_OUTPUT_FILE = "data/privacy_filtered/anonymous_customers.csv"

ORDER_OUTPUT_FILE = "data/privacy_filtered/anonymous_orders.csv"

PAYMENT_OUTPUT_FILE = "data/privacy_filtered/anonymous_payments.csv"

PURCHASE_HISTORY_OUTPUT_FILE = "data/privacy_filtered/anonymous_purchase_history.csv"


MIN_TEMPORAL_OFFSET_DAYS = -365
MAX_TEMPORAL_OFFSET_DAYS = 365


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
    "Total",                    # Total retained for downstream behavioral feature engineering.
                                # Required for AverageOrderValueTrend generation.
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
# DATASET
def configure_dataset(dataset):
    
    if dataset == "operational":
        customer_file = os.getenv("NORTHSTAR_CUSTOMER_FILE")
        order_file = os.getenv("NORTHSTAR_ORDER_FILE")
        payment_file = os.getenv("NORTHSTAR_PAYMENT_FILE")
        
    elif dataset == "training":
        customer_file = os.getenv("NORTHSTAR_TRAINING_CUSTOMER_FILE")
        order_file = os.getenv("NORTHSTAR_TRAINING_ORDER_FILE")
        payment_file = os.getenv("NORTHSTAR_TRAINING_PAYMENT_FILE")
        
    else:
        raise ValueError(
            f"Unknown dataset: {dataset}"
        )

    #Validate required environment variables
    if customer_file is None:
        raise RuntimeError(
            f"Missing customer file configuration for dataset: {dataset}"
        )
        
    if order_file is None:
        raise RuntimeError(
                    f"Missing order file configuration for dataset: {dataset}"
                )
        
    if payment_file is None:
        raise RuntimeError(
                    f"Missing payment file configuration for dataset: {dataset}"
                )
            
    return customer_file, order_file, payment_file


# LOADING
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

# TEMPORAL OFFSET MAPPING
def generate_temporal_offset_mapping(
    customer_data,
    anonymous_customer_map
):
    customer_temporal_offset_map = {}
    
    for customer in customer_data:
        customer_id = customer["CustomerID"]
        anonymous_customer_key = anonymous_customer_map[customer_id]
        temporal_offset_days = random.randint(
            MIN_TEMPORAL_OFFSET_DAYS,
            MAX_TEMPORAL_OFFSET_DAYS
        )
        customer_temporal_offset_map[
            anonymous_customer_key
        ] = temporal_offset_days
    
    return customer_temporal_offset_map



# DATETIME SHIFT
def shift_datetime(date_string, temporal_offset_days):
    date_object = datetime.strptime(
        date_string,
        "%Y-%m-%d %H:%M:%S"
    )

    shifted_datetime_object = date_object + timedelta(
        days=temporal_offset_days
    )

    return shifted_datetime_object.strftime("%Y-%m-%d %H:%M:%S")


# DATE SHIFT
def shift_date(date_string, temporal_offset_days):
    date_object = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    )

    shifted_date_object = date_object + timedelta(
        days=temporal_offset_days
    )

    return shifted_date_object.strftime("%Y-%m-%d")
    
# CUSTOMER FILTER
def filter_customer_data(
    customer_data,
    anonymous_customer_map,
    customer_temporal_offset_map
):
    
    privacy_filtered_customer_data = []

    for customer in customer_data:
        customer_id = customer["CustomerID"]
        anonymous_customer_key = anonymous_customer_map[customer_id]
        temporal_offset_days = customer_temporal_offset_map[anonymous_customer_key]
        privacy_filtered_customer = {
            "AnonymousCustomerKey": anonymous_customer_key,
            "JoinDate": shift_date(
                customer["JoinDate"],
                temporal_offset_days
            )
        }
        privacy_filtered_customer_data.append(privacy_filtered_customer)
    
    return privacy_filtered_customer_data


# ORDERS FILTER
def filter_order_data(
    order_data, 
    anonymous_customer_map,
    anonymous_order_map,
    customer_temporal_offset_map
):
    
    privacy_filtered_order_data = []

    for order in order_data:
        order_id = order["OrderID"]
        customer_id = order["CustomerID"]
        anonymous_customer_key = anonymous_customer_map[customer_id]
        temporal_offset_days = customer_temporal_offset_map[
            anonymous_customer_key
        ]
        anonymous_order_key = anonymous_order_map[order_id]
        privacy_filtered_order = {
            "AnonymousOrderKey": anonymous_order_key,
            "AnonymousCustomerKey": anonymous_customer_key,
            "OrderDateTime": shift_datetime(
                order["OrderDateTime"],
                temporal_offset_days
            ),
            "Total": order["Total"]
        }
        privacy_filtered_order_data.append(privacy_filtered_order)
    
    return privacy_filtered_order_data


# PAYMENTS FILTER
def filter_payment_data(
    payment_data,
    anonymous_order_map,
    privacy_filtered_order_data,
    customer_temporal_offset_map
):

    privacy_filtered_payment_data = []
    order_customer_lookup = {}

    for order in privacy_filtered_order_data:
        anonymous_order_key = order["AnonymousOrderKey"]
        anonymous_customer_key = order["AnonymousCustomerKey"]

        order_customer_lookup[anonymous_order_key] = anonymous_customer_key

    for payment in payment_data:
        order_id = payment["OrderID"]

        anonymous_order_key = anonymous_order_map[order_id]

        anonymous_customer_key = order_customer_lookup[
            anonymous_order_key
        ]

        temporal_offset_days = customer_temporal_offset_map[
            anonymous_customer_key
        ]

        payment_attempt = payment["PaymentAttempt"]
        payment_status = payment["PaymentStatus"]

        privacy_filtered_payment = {
            "AnonymousOrderKey": anonymous_order_key,
            "PaymentAttempt": payment_attempt,
            "PaymentDateTime": shift_datetime(
                payment["PaymentDateTime"],
                temporal_offset_days
            ),
            "PaymentStatus": payment_status
        }

        privacy_filtered_payment_data.append(
            privacy_filtered_payment
        )

    return privacy_filtered_payment_data

# MERGE ANONYMOUS DATA
def reconstruct_purchase_history(
    privacy_filtered_customer_data,
    privacy_filtered_order_data,
    privacy_filtered_payment_data
):

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
       
    # Load customers
    customer_data = load_csv(customer_file)
    
    # Load orders
    order_data = load_csv(order_file)
    
    # Load payments
    payment_data = load_csv(payment_file)
    
    
    # Generate anonymous mapping
    anonymous_customer_map = generate_anonymous_customer_mapping(customer_data)
    anonymous_order_map = generate_anonymous_order_mapping(order_data)
    customer_temporal_offset_map = generate_temporal_offset_mapping(
        customer_data,
        anonymous_customer_map
    )
    
    # Filter customer data
    privacy_filtered_customer_data = filter_customer_data(
        customer_data,
        anonymous_customer_map,
        customer_temporal_offset_map
    )
    
    # Filter order data
    privacy_filtered_order_data = filter_order_data(
        order_data,
        anonymous_customer_map,
        anonymous_order_map,
        customer_temporal_offset_map
    )
    
    # Filter payment data
    privacy_filtered_payment_data = filter_payment_data(
    payment_data,
    anonymous_order_map,
    privacy_filtered_order_data,
    customer_temporal_offset_map
)
    
    # Reconstruct purchase history
    anonymous_purchase_history_data = reconstruct_purchase_history(
        privacy_filtered_customer_data,
        privacy_filtered_order_data,
        privacy_filtered_payment_data
    )
 
     
    # QA Validation
    
    
    # Save anonymized datasets
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

    customer_file, order_file, payment_file = configure_dataset(
        DATASET
    )

    main(
        customer_file,
        order_file,
        payment_file,
    )