"""
===============================================================================
Project:        Project NorthStar
Engine:         NorthStar Commerce Training Population Generator
File:           generate_training_population.py
Author:         Mat Thompson
Created:        2026-08-17
Version:        1.0

Purpose:
    Generate an independent synthetic training population for machine
    learning by configuring and orchestrating the NorthStar Commerce
    Generation Engine.

    This generator creates a completely separate enterprise population
    from the operational dataset while reusing the same business rules
    and generation logic. The resulting data serves as the foundation
    for downstream feature engineering and machine learning.

Inputs:
    - Training configuration
    - Shared Generation Engine
    - Business rules
    - Probability distributions

Outputs:
    - training_customers.csv
    - training_categories.csv
    - training_products.csv
    - training_orders.csv
    - training_order_items.csv
    - training_payments.csv

Current Responsibilities:
    - Configure an independent training universe.
    - Invoke the shared Generation Engine.
    - Generate synthetic training datasets.
    - Export training datasets.

Non-Responsibilities:
    - Business rule implementation
    - Data quality validation
    - Privacy protection
    - Data standardization
    - Feature engineering
    - Machine learning
    - Predictive analytics

Engineering Laws:
    1. Never duplicate Generation Engine logic.
    2. Configuration defines the universe.
    3. The Generation Engine defines the laws of physics.
    4. Training populations must remain independent of operational data.
    5. Every generated dataset must be reproducible from configuration.

Architecture:

            Training Configuration
                      │
                      ▼
     Training Population Generator
                      │
                      ▼
      NorthStar Commerce Generation Engine
                      │
                      ▼
      Independent Synthetic Training Dataset

===============================================================================
"""

from generate_ecommerce_data import (
    generate_customers,
    generate_categories,
    generate_products,
    generate_orders,
    generate_order_items,
    finalize_orders,
    generate_payments,
    build_order_items_lookup,
    build_product_lookup,
    write_csv,
)

from datetime import date
from pathlib import Path
import random



# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAINING_DATA_FOLDER = (
    PROJECT_ROOT / "data" / "training_source"
)

TRAINING_DATA_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# TRAINING CONFIGURATION
# =============================================================================

TRAINING_RANDOM_SEED = 8675309
TRAINING_START_DATE = date(2023, 1, 1)
TRAINING_END_DATE =  date.today()
TRAINING_NUMBER_OF_CUSTOMERS = 5000

# =============================================================================
# OUTPUT FILES
# =============================================================================

TRAINING_CUSTOMER_FILE = TRAINING_DATA_FOLDER / "training_customer.csv"
TRAINING_CATEGORIES_FILE = TRAINING_DATA_FOLDER / "training_categories.csv"
TRAINING_PRODUCTS_FILE = TRAINING_DATA_FOLDER / "training_products.csv"
TRAINING_ORDERS_FILE = TRAINING_DATA_FOLDER / "training_orders.csv"
TRAINING_ORDER_ITEMS_FILE = TRAINING_DATA_FOLDER / "training_order_items.csv"
TRAINING_PAYMENTS_FILE = TRAINING_DATA_FOLDER / "training_payments.csv"

# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    
    random.seed(TRAINING_RANDOM_SEED)
   
    customers = generate_customers(
        TRAINING_NUMBER_OF_CUSTOMERS,
        TRAINING_START_DATE,
        TRAINING_END_DATE,
    )

    categories = generate_categories()
    
    products = generate_products(
        categories,
        TRAINING_END_DATE,
    )
    
    orders = generate_orders(
        customers,
        TRAINING_START_DATE,
        TRAINING_END_DATE,
    )
    
    order_items = generate_order_items(
        orders,
        products,
    )
    
    order_items_lookup = build_order_items_lookup(
        order_items
    )
    
    customer_lookup = {
        customer["CustomerID"]: customer
        for customer in customers
    }
    
    orders = finalize_orders(
        orders,
        order_items_lookup,
        customer_lookup,
            
    )
    
    payments = generate_payments(
        orders,
    )
    
# =============================================================================
# write CSV
# =============================================================================
    write_csv(
        TRAINING_CUSTOMER_FILE,
        customers,
        [
            "CustomerID",
            "FirstName",
            "LastName",
            "Email",
            "Phone",
            "City",
            "State",
            "Region",
            "BirthYear",
            "Gender",
            "JoinDate",
            "CustomerSegment",
            "LoyaltyTier",
            "ShoppingProfile",
            "IsActive",
        ],
    )

    write_csv(
        TRAINING_CATEGORIES_FILE,
        categories,
        [
            "CategoryID",
            "CategoryName",
        ],
    )

    write_csv(
        TRAINING_PRODUCTS_FILE,
        products,
        [
            "ProductID",
            "CategoryID",
            "ProductName",
            "UnitPrice",
            "UnitCost",
            "LaunchDate",
            "IsActive",
        ],
    )

    write_csv(
        TRAINING_ORDERS_FILE,
        orders,
        [
            "OrderID",
            "CustomerID",
            "OrderDateTime",
            "Subtotal",
            "DiscountRate",
            "DiscountAmount",
            "ShippingMethod",
            "Shipping",
            "Tax",
            "Total",
        ],
    )

    write_csv(
        TRAINING_ORDER_ITEMS_FILE,
        order_items,
        [
            "OrderItemID",
            "OrderID",
            "ProductID",
            "Quantity",
            "UnitPrice",
            "LineTotal",
        ],
    )

    write_csv(
        TRAINING_PAYMENTS_FILE,
        payments,
        [
            "PaymentID",
            "OrderID",
            "PaymentAttempt",
            "PaymentDateTime",
            "PaymentMethod",
            "PaymentAmount",
            "PaymentStatus",
        ],
    )

    print("Training population created successfully:")
    print(f"- Customers: {len(customers):,}")
    print(f"- Categories: {len(categories):,}")
    print(f"- Products: {len(products):,}")
    print(f"- Orders: {len(orders):,}")
    print(f"- Order Items: {len(order_items):,}")
    print(f"- Payments: {len(payments):,}")
    
    
    
    
if __name__ == "__main__":
    main()