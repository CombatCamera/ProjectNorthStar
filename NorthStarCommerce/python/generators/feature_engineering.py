"""
===============================================================================
Project NorthStar
Feature Engineering Engine
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-19
Version: 1.0

Purpose:
Generate reusable business features from QA-certified business events by
transforming raw operational data into machine learning-ready evidence.

Business Objective:
Produce reusable evidence that supports predictive analytics while maintaining
clear separation between feature generation, business interpretation, and
machine learning.

Core Responsibilities:
- Generate reusable business features.
- Organize features into logical feature families.
- Build progressively richer evidence from previously assembled features.
- Assemble the customer behavior feature dataset.
- Support machine learning and future analytical engines.

Core Feature Families:
- Temporal Features
- Purchase Features
- Behavior Features
- Payment Features (Future)

Version 1 Core Evidence Bricks:
- DaysSinceLastPurchase
- AvgDaysBetweenPurchases
- PercentBeyondHealthyWindow
- PurchaseFrequencyTrend
- AverageOrderValueTrend

Engineering Principles:
- Every feature is the answer to a business question.
- Build reusable business knowledge, not model-specific features.
- Feature families organize the code; business questions organize the thinking.
- Once evidence has been assembled, downstream feature families reuse it
  instead of recalculating business logic.
- Knowledge flows forward through the pipeline.
- Debugging outputs are optional and controlled through configuration.

Output:
customer_behavior_features.csv

Future Expansion:
This engine is designed to support additional feature families, contextual
(real-world) data sources, and future analytical engines without redesigning
the core architecture.
===============================================================================
"""

import pandas as pd
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

# Dataset Selection

# DATASET = "operational"
DATASET = "training"

# Debug Mode

DEBUG_MODE = True


# Output Paths


# Minimum Reliable History

MINIMUM_RELIABLE_HISTORY = 10


# Required Columns

REQUIRED_CUSTOMER_COLUMNS = [
    "AnonymousCustomerKey",
    "JoinDate",
]

REQUIRED_ORDER_COLUMNS = [
    "AnonymousOrderKey",
    "AnonymousCustomerKey",
    "OrderDateTime",
    "Total",
]

REQUIRED_PAYMENT_COLUMNS = [
    "AnonymousOrderKey",
    "PaymentStatus",
]



# =============================================================================
# LOAD DATA
# =============================================================================

'''
Load all required datasets for Feature Engineering.
'''
def load_data(
    customers_file,
    orders_file,
    payments_file,
):
    customers_df = pd.read_csv(customers_file)
    orders_df = pd.read_csv(orders_file)
    payments_df = pd.read_csv(payments_file)
    
    return (
        customers_df,
        orders_df,
        payments_df,
    )


# =============================================================================
# INPUT VALIDATION
# =============================================================================

'''
Validate the inputs for required data.
'''
def validate_required_columns(df, required_columns, dataset_name):
    
    missing_columns = []
    
    for column in required_columns:
        if column not in df.columns:
           missing_columns.append(column)
        
    if missing_columns:
        raise RuntimeError(
            f"{dataset_name} is missing required columns: "
            f"{missing_columns}"
        )


def validate_dataframe_not_empty(df, dataset_name):

    if df.empty:
        raise RuntimeError(
            f"{dataset_name} is empty."
        )
    return


def validate_inputs(
    customers_df,
    orders_df,
    payments_df,
):

    # Customer required columns
    validate_dataframe_not_empty(
        customers_df,
        "customers",
    )
    
    validate_required_columns(
        customers_df,
        REQUIRED_CUSTOMER_COLUMNS,
        "customers"
    )
    
    
    # Orders required columns
    validate_dataframe_not_empty(
        orders_df,
        "orders",
    )
    
    validate_required_columns(
        orders_df,
        REQUIRED_ORDER_COLUMNS,
        "orders"
    )
    
    
    # Payments required columns
    validate_dataframe_not_empty(
        payments_df,
        "payments",
    )
    
    validate_required_columns(
        payments_df,
        REQUIRED_PAYMENT_COLUMNS,
        "payments"
    )
    
    
    if DEBUG_MODE:
        print("✓ Customers validated")
        print("✓ Orders validated")
        print("✓ Payments validated")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
'''
Switches between operational and training datasets.
'''
def configure_dataset(dataset):
    
    if dataset == "operational":
        customers_file = os.getenv("NORTHSTAR_CUSTOMER_FILE")
        orders_file = os.getenv("NORTHSTAR_ORDER_FILE")
        payments_file = os.getenv("NORTHSTAR_PAYMENT_FILE")
    elif dataset == "training":
        customers_file = os.getenv("NORTHSTAR_ANONYMIZED_CUSTOMER_FILE")
        orders_file = os.getenv("NORTHSTAR_ANONYMIZED_ORDER_FILE")
        payments_file = os.getenv("NORTHSTAR_ANONYMIZED_PAYMENT_FILE")
    else:
        raise ValueError(
            f"Unknown dataset: {dataset}"
        )
    
    return (
        customers_file,
        orders_file,
        payments_file,
    )


def generate_successful_purchase_history(orders_df, payments_df):

    merged_df = pd.merge(
        orders_df,
        payments_df,
        on="AnonymousOrderKey",
    ) 

    purchase_history = merged_df[
        merged_df["PaymentStatus"] == "Successful"
    ]
    
    successful_purchase_history = purchase_history[
        [
            "AnonymousCustomerKey",
            "AnonymousOrderKey",
            "OrderDateTime",
            "Total",
        ]
    ].copy()

    successful_purchase_history["OrderDateTime"] = pd.to_datetime(
        successful_purchase_history["OrderDateTime"]
    )

    print(successful_purchase_history["OrderDateTime"].dtype)
    
    
    return successful_purchase_history

# =============================================================================
# FEATURE FAMILIES
# =============================================================================
     
# Generate reusable time-based customer behavior features that describe
# a customer's purchasing history and current purchasing state.
def generate_temporal_features(successful_purchase_history):
    
    customer_groups = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    )
    

    last_purchase_dates = customer_groups["OrderDateTime"].max()
    
    
    
    print(last_purchase_dates)
    print(last_purchase_dates.dtype)
    
    
def generate_purchase_features():
    pass



def generate_behavior_features():
    pass




# =============================================================================
# ASSEMBLER
# =============================================================================

def assemble_feature_dataset():
    pass




# =============================================================================
# MAIN
# =============================================================================

def main():
    # Select data
    (
        customers_file,
        orders_file,
        payments_file,
    ) = configure_dataset(DATASET)
    

    # Load data
    (
        customers_df,
        orders_df,
        payments_df,
    ) = load_data(
        customers_file,
        orders_file,
        payments_file,
    )
  
    
    # Validation
    validate_inputs(
        customers_df,
        orders_df,
        payments_df,
    )
    
    
    # Call helpers
    successful_purchase_history = generate_successful_purchase_history(
        orders_df, payments_df,
    )



    # Generate temporal features
    temporal_features = generate_temporal_features(
        successful_purchase_history
    )
    
    
    
    # Assemble dataset
    
    # Savee output
    

if __name__ == "__main__":
    main()