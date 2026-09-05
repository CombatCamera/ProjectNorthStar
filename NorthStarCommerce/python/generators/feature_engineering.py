"""
===============================================================================
Project NorthStar
Feature Engineering Engine
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-19
Last Updated: 2026-08-25
Version: 1.1

Purpose:
Generate reusable business features from QA-certified business events by
transforming operational and privacy-preserved data into machine learning-ready
evidence.

Business Objective:
Produce reusable evidence that supports predictive analytics while maintaining
clear separation between business data preparation, feature generation,
business interpretation, and machine learning.

Core Responsibilities:
- Generate reusable business features.
- Organize features into logical feature families.
- Prepare reusable business data objects for downstream feature generation.
- Build progressively richer evidence from previously assembled business data.
- Assemble the customer behavior feature dataset.
- Support current-state and historical observation-based feature generation.
- Prevent future information from entering historical feature calculations.
- Support machine learning and future analytical engines.

Core Feature Families:
- Temporal Features
- Purchase Features
- Behavior Features
- Payment Features (Future)

Business Data Preparation:
- Successful Purchase History
- Purchase History As Of Observation Date
- Purchase Intervals
- Purchase Interval Changes

Version 1.1 Core Evidence:
- DaysSinceLastPurchase
- AverageDaysBetweenPurchases
- SuccessfulOrderCount
- AverageOrderValue
- PurchaseFrequency
- PurchaseIntervalStdDev
- AverageIntervalChange

Historical Observation Support:
Feature generation can be anchored to a defined observation date. Only
business events known on or before that observation date may contribute to
historical feature calculations.

Historical Data Rule:
    OrderDateTime <= ObservationDate

This boundary prevents future information from leaking into historical model
evidence and supports the creation of time-valid machine learning training
examples.

Engineering Principles:
- Every feature is the answer to a business question.
- Build reusable business knowledge, not model-specific features.
- Feature families organize the code; business questions organize the thinking.
- Business Data Preparation creates reusable business objects before feature
  generation.
- Once evidence has been assembled, downstream feature families reuse it
  instead of recalculating business logic.
- Knowledge flows forward through the pipeline.
- Historical features may use only information available as of the observation
  date.
- Prefer the simplest design that remains clear, maintainable, and teachable.
- Debugging outputs are optional and controlled through configuration.

Output:
customer_behavior_features.csv

Future Expansion:
This engine is designed to support historical training population generation,
additional feature families, contextual real-world data sources, and future
analytical engines without redesigning the core architecture.
===============================================================================
"""

import pandas as pd
import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# ========================================================
# CONFIGURATION
# ========================================================

# Dataset Selection

# DATASET = "operational"
DATASET = "training"

# Debug Mode

DEBUG_MODE = True

# Minimum Reliable History

MINIMUM_RELIABLE_HISTORY = 10

# Rounding Precision
CURRENCY_PRECISION = Decimal("0.01")

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



# ========================================================
# LOAD DATA
# ========================================================

# Load all required datasets for Feature Engineering.

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

# ========================================================
# INPUT VALIDATION
# ========================================================

# Validate the inputs for required data.

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
    verbose=True,
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
    
    
    if DEBUG_MODE and verbose:
        print("✓ Customers validated")
        print("✓ Orders validated")
        print("✓ Payments validated")

# ========================================================
# HELPER FUNCTIONS
# ========================================================

# Switches between operational and training datasets.

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


def round_currency(value):
    value = Decimal(str(value))
    
    return value.quantize(
        CURRENCY_PRECISION,
        rounding=ROUND_HALF_UP
    )
     
# ========================================================
# # Write Output
# ========================================================

def save_feature_dataset(feature_dataset, output_path):
    feature_dataset.to_csv(
        output_path,
        index=False,
)

# ========================================================
# Business Data Preparation
# ========================================================

def generate_successful_purchase_history(orders_df, payments_df):

    successful_payments = payments_df[
        payments_df["PaymentStatus"] == "Successful"
    ][
        ["AnonymousOrderKey"]
    ].drop_duplicates()

    purchase_history = pd.merge(
        orders_df,
        successful_payments,
        on="AnonymousOrderKey",
    )
    
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
   
    return successful_purchase_history


def generate_purchase_history_as_of(
    successful_purchase_history,
    observation_date,
):
    
    generate_purchase_history_as_of = successful_purchase_history[
        successful_purchase_history["OrderDateTime"] <= observation_date
    ].copy()

    return generate_purchase_history_as_of


def generate_purchase_intervals(successful_purchase_history):
    
    purchase_intervals = successful_purchase_history[
        [
            "AnonymousCustomerKey",
            "OrderDateTime",
        ]
    ].copy()
    
    purchase_intervals = purchase_intervals.sort_values(
        by =[
            "AnonymousCustomerKey",
            "OrderDateTime"
        ]
    )
    
    customer_purchase_groups = purchase_intervals.groupby(
        "AnonymousCustomerKey"
    )
    
    previous_order_dates = customer_purchase_groups[
        "OrderDateTime"
    ].shift()
    
    days_between_purchases = (
            purchase_intervals["OrderDateTime"]
            - previous_order_dates
        ).dt.days
    
    days_between_purchases.name = "DaysBetweenPurchases"
    
    purchase_intervals["DaysBetweenPurchases"] = (
        days_between_purchases
    )
    
    return purchase_intervals
    
    
def generate_purchase_interval_changes(purchase_intervals):
    purchase_interval_changes = purchase_intervals.copy()
    
    purchase_interval_changes["PurchaseIntervalChange"] = (
        purchase_interval_changes
        .groupby("AnonymousCustomerKey")["DaysBetweenPurchases"]
        .diff()
    )
    
    return purchase_interval_changes
    
# ========================================================
# # FEATURE FAMILIES
# ========================================================
     
# Generate reusable time-based customer behavior features that describe
# a customer's purchasing history and current purchasing state.
def generate_temporal_features(
    successful_purchase_history,
    purchase_intervals,
    evaluation_date,
):
    
# Days since last purchase    
    customer_groups = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    )
    
    last_purchase_dates = customer_groups["OrderDateTime"].max()
    
    days_since_last_purchase = (
        evaluation_date
        - last_purchase_dates
    ).dt.days

    days_since_last_purchase.name = "DaysSinceLastPurchase"
    
    
# Average Days Between Purchases
    
    average_days_between_purchases = purchase_intervals.groupby(
        "AnonymousCustomerKey"
    )["DaysBetweenPurchases"].mean()
    
    average_days_between_purchases.name = "AverageDaysBetweenPurchases"
    
    
# Build Temporal features

    days_since_last_purchase = days_since_last_purchase.reset_index()
    
    average_days_between_purchases = (
        average_days_between_purchases.reset_index()
    )
    
    temporal_features = pd.merge(
        days_since_last_purchase,
        average_days_between_purchases,
        on="AnonymousCustomerKey",
        how="left",
    )
       
    return temporal_features
    
    
def generate_purchase_features(successful_purchase_history,):
    
# Successful Order Count

    successful_order_count = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    ).size()
    
    successful_order_count.name = "SuccessfulOrderCount"
    

# Average Order Value
    average_order_value = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    )["Total"].mean()

    average_order_value.name = ("AverageOrderValue")
    
    average_order_value = average_order_value.apply(
        round_currency
    )


# Purchase Frequency

    first_purchase_date = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    )["OrderDateTime"].min()
    
    last_purchase_date = successful_purchase_history.groupby(
        "AnonymousCustomerKey"
    )["OrderDateTime"].max()
    
    active_purchase_days = (
        last_purchase_date
        - first_purchase_date
    ).dt.days

    purchase_frequency = (
        successful_order_count
        / active_purchase_days.replace(0, pd.NA)
    )
    
    purchase_frequency.name = ("PurchaseFrequency")


# Assemble Purchase Features
    successful_order_count = (
        successful_order_count.reset_index()
    )
     
    average_order_value = (
        average_order_value.reset_index()
    )
    
    purchase_frequency = (
        purchase_frequency.reset_index()
    )

    purchase_features = pd.merge(
        successful_order_count,
        average_order_value,
        on="AnonymousCustomerKey"
    )

    purchase_features = pd.merge(
        purchase_features,
        purchase_frequency,
        on="AnonymousCustomerKey"
    )

    return purchase_features

# Behavior Features

def meets_minimum_reliable_history(history):

    number_of_intervals = history.notna().sum()

    return number_of_intervals >= MINIMUM_RELIABLE_HISTORY
    
    
def generate_purchase_interval_stddev(purchase_intervals):
    
    # Minimum Reliable History
    if not meets_minimum_reliable_history(purchase_intervals):
        return pd.NA

    # Purchase Interval Standard Deviation
    return purchase_intervals.std()


def generate_average_interval_change(purchase_interval_changes):
    
    # Minimum Reliable History
    if not meets_minimum_reliable_history(
        purchase_interval_changes["DaysBetweenPurchases"]
    ):
        return pd.NA
    
    # Average Purchase Interval Change
    return purchase_interval_changes["PurchaseIntervalChange"].mean()


def generate_behavior_features(
    purchase_intervals, 
    purchase_interval_changes
):
    
    behavior_records = []
    
    # Group Customers
    for customer_key in purchase_intervals["AnonymousCustomerKey"].unique():
        customer_intervals = purchase_intervals[
            purchase_intervals["AnonymousCustomerKey"] == customer_key
        ]
    
        customer_interval_changes = purchase_interval_changes[
            purchase_interval_changes["AnonymousCustomerKey"] == customer_key
        ]
        
        # For Each Customer, Calculate Features
        purchase_interval_stddev = generate_purchase_interval_stddev(
            customer_intervals["DaysBetweenPurchases"]
        )
    
        average_interval_change = generate_average_interval_change(
            customer_interval_changes
        )
        
        customer_behavior_record = {
            "AnonymousCustomerKey": customer_key,
            "PurchaseIntervalStdDev": purchase_interval_stddev,
            "AverageIntervalChange": average_interval_change
        }
        
        # Append
        behavior_records.append(customer_behavior_record)
    
    
    # Return DataFrame
    return pd.DataFrame(behavior_records)
                    
# ========================================================
# ASSEMBLER
# ========================================================

def assemble_feature_dataset(
    temporal_features, 
    purchase_features, 
    behavior_features 
):
    
    feature_dataset = temporal_features.merge(
        purchase_features,
        on="AnonymousCustomerKey",
        how="left",
    )

    feature_dataset = feature_dataset.merge(
        behavior_features,
        on="AnonymousCustomerKey",
        how="left",
    )

    return feature_dataset

# ========================================================
# Feature Pipeline
# ========================================================

def build_feature_dataset(
    observation_date=None,
    verbose=True,
):
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
        verbose=verbose,
    )
    
    
    # Call Business Data Preparation
    successful_purchase_history = generate_successful_purchase_history(
        orders_df, 
        payments_df,
    )
    
    
    if observation_date is None:
        evaluation_date = datetime.now()
    else:
        evaluation_date = pd.to_datetime(observation_date)
        
        
    purchase_history_as_of = generate_purchase_history_as_of(
        successful_purchase_history,
        evaluation_date,
    )
    
    qa_purchase_history = purchase_history_as_of

    purchase_intervals = generate_purchase_intervals(
        purchase_history_as_of
    )

    purchase_interval_changes = generate_purchase_interval_changes(
        purchase_intervals
    )

    



    # Generate temporal features
    temporal_features = generate_temporal_features(
        purchase_history_as_of,
        purchase_intervals,
        evaluation_date,
    )
    
    # Generate Purchase Features
    purchase_features = generate_purchase_features(
        purchase_history_as_of,
    )
    
    # Generate Behavior Features
    behavior_features = generate_behavior_features(
        purchase_intervals,
        purchase_interval_changes
    )
    
    # Assemble dataset
    feature_dataset = assemble_feature_dataset(
        temporal_features,
        purchase_features,
        behavior_features
    )

    return feature_dataset, qa_purchase_history

# ========================================================
# Main
# ========================================================

def main():
    
    
    feature_dataset, successful_purchase_history = build_feature_dataset()


if __name__ == "__main__":
    main()