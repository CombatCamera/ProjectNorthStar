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

# Output Paths

# Minimum Reliable History
MINIMUM_RELIABLE_HISTORY = 10

# =============================================================================
# LOAD DATA
# =============================================================================

NORHTSTAR_CUSTOMERS_FILE = ""
NORTHSTAR_ORDERS_FILE = ""
NORTHSTAR_PAYMENTS_FILE = ""
NORTHSTAR_ORDER_ITEMS_FILE = ""

# =============================================================================
# INPUT VALIDATION
# =============================================================================



# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def configure_dataset(dataset):
    
    if dataset == "operational":
        customers_file = os.getenv("NORTHSTAR_CUSTOMER_FILE")
        orders_file = os.getenv("NORTHSTAR_ORDER_FILE")
        payments_file = os.getenv("NORTHSTAR_PAYMENT_FILE")
        order_items_file = os.getenv("NORTHSTAR_ORDER_ITEMS_FILE")
    elif dataset == "training":
        customers_file = os.getenv("NORTHSTAR_TRAINING_CUSTOMER_FILE")
        orders_file = os.getenv("NORTHSTAR_TRAINING_ORDER_FILE")
        payments_file = os.getenv("NORTHSTAR_TRAINING_PAYMENT_FILE")
        order_items_file = os.getenv("NORTHSTAR_TRAINING_ORDER_ITEMS_FILE")
    else:
        raise ValueError(
            f"Unknown dataset: {dataset}"
        )
    
    return (
        customers_file,
        orders_file,
        payments_file,
        order_items_file,
    )


'''
Load all required datasets for Feature Engineering.
'''
def load_data(
    customers_file,
    orders_file,
    payments_file,
    order_items_file,
):
    customers_df = pd.read_csv(customers_file)
    orders_df = pd.read_csv(orders_file)
    payments_df = pd.read_csv(payments_file)
    order_items_df = pd.read_csv(order_items_file)
    
    return (
        customers_df,
        orders_df,
        payments_df,
        order_items_df
    )

# =============================================================================
# FEATURE FAMILIES
# =============================================================================
     
# Generate reusable time-based customer behavior features that describe
# a customer's purchasing history and current purchasing state.
def generate_temporal_features():
    pass
    
    

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
        order_items_file,
    ) = configure_dataset(DATASET)
    

    # Load data
    (
        customers_df,
        orders_df,
        payments_df,
        order_items_df,
    ) = load_data(
        customers_file,
        orders_file,
        payments_file,
        order_items_file,
    )

    print(customers_df.head())
    print(orders_df.head())
    print(payments_df.head())
    print(order_items_df.head())
    # Generate temporal features
    
    # Assemble dataset
    
    # Savee output
    

if __name__ == "__main__":
    main()