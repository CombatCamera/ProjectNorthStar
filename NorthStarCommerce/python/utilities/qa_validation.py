"""
===============================================================================
Project:        Project NorthStar
Engine:         NorthStar Commerce QA Engine
File:           qa_validation.py
Author:         Mat Thompson
Created:        2026-08-03
Last Updated:   2026-08-17
Version:        2.0

Purpose:
    Validate the integrity, consistency, and business correctness of
    NorthStar Commerce datasets before they are used for downstream
    analytics, privacy protection, feature engineering, or machine
    learning.

    The QA Engine verifies that synthetic datasets satisfy business
    rules, maintain referential integrity, and accurately represent
    a realistic enterprise environment.

Inputs:
    - Dataset configuration
    - Customer dataset
    - Product dataset
    - Order dataset
    - Order Item dataset
    - Payment dataset
    - Optional Shipment dataset

Outputs:
    - QA validation report
    - Dataset certification
    - PASS / FAIL status

Current Responsibilities:
    - Validate referential integrity.
    - Validate financial integrity.
    - Validate timeline consistency.
    - Validate business rules.
    - Validate shipment lifecycle (when applicable).
    - Certify datasets for downstream processing.

Non-Responsibilities:
    - Data generation
    - Privacy protection
    - Data standardization
    - Feature engineering
    - Machine learning
    - Predictive analytics

Engineering Laws:
    1. Validate datasets without modifying them.
    2. Validate only the datasets that exist.
    3. Every validation must be deterministic.
    4. Certification requires all applicable checks to pass.
    5. Validation rules represent business truth.

Architecture:

                    Dataset Configuration
                             │
                             ▼
              NorthStar Commerce QA Engine
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
    Operational Dataset             Training Dataset
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                   Dataset Certification

===============================================================================
"""

import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# =============================================================================
# DATASET TO VALIDATE
# =============================================================================

# DATASET = "operational"
DATASET = "training"

# ========================================================= 
# REPORT SETTINGS
# =========================================================

REPORT_WIDTH = 85
CURRENCY_PRECISION = Decimal("0.01")

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

TRAINING_DATA_FOLDER = PROJECT_ROOT / "data" / "training_source"


CUSTOMERS_FILE = DATA_FOLDER / "customers.csv"
PRODUCTS_FILE = DATA_FOLDER / "products.csv"
ORDERS_FILE = DATA_FOLDER / "orders.csv"
ORDER_ITEMS_FILE = DATA_FOLDER / "order_items.csv"
PAYMENTS_FILE = DATA_FOLDER / "payments.csv"
SHIPMENTS_FILE = DATA_FOLDER / "shipments.csv"

TRAINING_CUSTOMERS_FILE = TRAINING_DATA_FOLDER / "training_customer.csv"
TRAINING_PRODUCTS_FILE = TRAINING_DATA_FOLDER / "training_products.csv"
TRAINING_ORDERS_FILE = TRAINING_DATA_FOLDER / "training_orders.csv"
TRAINING_ORDER_ITEMS_FILE = TRAINING_DATA_FOLDER / "training_order_items.csv"
TRAINING_PAYMENTS_FILE = TRAINING_DATA_FOLDER / "training_payments.csv"
  
    

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def round_currency(value):
    return value.quantize(
        CURRENCY_PRECISION,
        rounding=ROUND_HALF_UP
    )

def load_csv(file_path):    
    
    records = []
    
    with file_path.open(
            mode="r",
            newline= "",
            encoding="utf-8-sig",
        ) as csv_file:
    
        reader = csv.DictReader(csv_file)
    
        for row in reader:
            records.append(row)
        
    return records


def build_order_items_lookup(order_items):
    """Group all order items by OrderID."""
    order_items_lookup = {}
    
    for item in order_items:
        order_id = item["OrderID"]
        
        if order_id not in order_items_lookup:
            order_items_lookup[order_id] = []
            
        order_items_lookup[order_id].append(item)
        
    return order_items_lookup


def build_order_id_counts(orders):
    
    order_id_counts = {}
    
    for order in orders:
        order_id = order["OrderID"]
        
        if order_id not in order_id_counts:
            order_id_counts[order_id] = 1
        else:    
            order_id_counts[order_id] += 1

    return order_id_counts



def get_duplicate_order_ids(order_id_counts):
    
    duplicate_order_ids = []
    
    for order_id, count in order_id_counts.items():
        if count > 1:
            duplicate_order_ids.append(
                {
                    "OrderID": order_id,
                    "Occurrences": count
                }
            )

    return duplicate_order_ids


def build_payments_lookup(payments):
    """Group all payments by OrderID."""
    payments_lookup = {}
    
    for payment in payments:
        order_id = payment["OrderID"]
        
        if order_id not in payments_lookup:
            payments_lookup[order_id] = []
            
        payments_lookup[order_id].append(payment)
        
    return payments_lookup


def build_products_lookup(products):
    """Create a lookup dictionary for products by ProductID."""
    products_lookup = {}
    
    for product in products:
        product_id = product["ProductID"]
        products_lookup[product_id] = product
        
    return products_lookup


def build_customers_lookup(customers):
    """Create a lookup dictionary for customers by CustomerID."""
    customers_lookup = {}
    
    for customer in customers:
        customer_id = customer["CustomerID"]
        customers_lookup[customer_id] = customer
        
    return customers_lookup


def build_orders_lookup(orders):
    """Create a lookup dictionary for orders by OrderID."""
    orders_lookup = {}
    
    for order in orders:
        order_id = order["OrderID"]
        orders_lookup[order_id] = order
        
    return orders_lookup


def build_successful_payments_lookup(payments):
    """Group all successful payments by OrderID."""
    successful_payments_lookup = {}
    
    for payment in payments:
        if payment["PaymentStatus"] == "Successful":
            order_id = payment["OrderID"]
            successful_payments_lookup[order_id] = payment
            
    return successful_payments_lookup
# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_orders_have_items(orders, order_items):
    
    order_items_lookup = build_order_items_lookup(order_items)
    orders_without_items = []
    
    for order in orders:
        order_id = order["OrderID"]
        
        if order_id not in order_items_lookup:
            orders_without_items.append(order)
    
    passed = len(orders_without_items) == 0
    
    return {
        "name": "Orders Have Items",
        "passed": passed,
        "records_checked": len(orders),
        "issues_found": len(orders_without_items),
        "details": (
            f"{len(orders):,} orders checked. "
            f"{len(orders_without_items):,} orders are missing items."
        )
    }

def validate_unique_order_ids(orders):
    order_id_counts = build_order_id_counts(orders)
    duplicate_order_ids = get_duplicate_order_ids(order_id_counts)
    
    passed = len(duplicate_order_ids) == 0
    
    return {
        "name": "Unique Order IDs",
        "passed": passed,
        "records_checked": len(orders),
        "issues_found": len(duplicate_order_ids),
        "details": (
            f"{len(orders):,} orders checked. "
            f"{len(duplicate_order_ids):,} duplicate order IDs found."
        )
    }


def validate_orders_have_payments(orders, payments):
    payments_lookup = build_payments_lookup(payments)
    orders_without_payments = []
    
    for order in orders:
        order_id = order["OrderID"]
        
        if order_id not in payments_lookup:
            orders_without_payments.append(order)
    
    passed = len(orders_without_payments) == 0
    
    return {
        "name": "Orders Have Payments",
        "passed": passed,
        "records_checked": len(orders),
        "issues_found": len(orders_without_payments),
        "details": (
            f"{len(orders):,} orders checked. "
            f"{len(orders_without_payments):,} orders are missing payments."
        )
    }
    
    
def validate_order_items_have_products(order_items, products):
    products_lookup = build_products_lookup(products)
    order_items_without_products = []
    
    for item in order_items:
        product_id = item["ProductID"]
        
        if product_id not in products_lookup:
            order_items_without_products.append(item)
    
    passed = len(order_items_without_products) == 0
    
    return {
        "name": "Order Items Have Products",
        "passed": passed,
        "records_checked": len(order_items),
        "issues_found": len(order_items_without_products),
        "details": (
            f"{len(order_items):,} order items checked. "
            f"{len(order_items_without_products):,} order items are missing products."
        )
    }
    
    
def validate_orders_have_customers(orders, customers):
    customers_lookup = build_customers_lookup(customers)
    orders_without_customers = []
    
    for order in orders:
        customer_id = order["CustomerID"]
        
        if customer_id not in customers_lookup:
            orders_without_customers.append(order)
    
    passed = len(orders_without_customers) == 0
    
    return {
        "name": "Orders Have Customers",
        "passed": passed,
        "records_checked": len(orders),
        "issues_found": len(orders_without_customers),
        "details": (
            f"{len(orders):,} orders checked. "
            f"{len(orders_without_customers):,} orders are missing customers."
        )
    }
    
    
def validate_payments_have_orders(payments, orders):
    orders_lookup = build_orders_lookup(orders)
    payments_without_orders = []
    
    for payment in payments:
        order_id = payment["OrderID"]
        
        if order_id not in orders_lookup:
            payments_without_orders.append(payment)
    
    passed = len(payments_without_orders) == 0
    
    return {
        "name": "Payments Have Orders",
        "passed": passed,
        "records_checked": len(payments),
        "issues_found": len(payments_without_orders),
        "details": (
            f"{len(payments):,} payments checked. "
            f"{len(payments_without_orders):,} payments are missing orders."
        )
    } 


def validate_payment_amounts_match_order_totals(orders, payments):
    orders_lookup = build_orders_lookup(orders)
    mismatched_payments = []

    for payment in payments:
        order_id = payment["OrderID"]
        order = orders_lookup.get(order_id)

        if order is None:
            continue

        payment_amount = float(payment["PaymentAmount"])
        order_total = float(order["Total"])

        if round(payment_amount, 2) != round(order_total, 2):
            mismatched_payments.append(
                {
                    "PaymentID": payment["PaymentID"],
                    "OrderID": order_id,
                    "PaymentAmount": payment_amount,
                    "OrderTotal": order_total,
                }
            )

    passed = len(mismatched_payments) == 0

    return {
        "name": "Payment Amounts Match Order Totals",
        "passed": passed,
        "records_checked": len(payments),
        "issues_found": len(mismatched_payments),
        "details": (
            f"{len(payments):,} payments checked. "
            f"{len(mismatched_payments):,} payments have mismatched amounts."
        ),
    }
    
def validate_order_totals_reconciled(orders, order_items):
    order_items_lookup = build_order_items_lookup(order_items)
    mismatched_orders = []

    for order in orders:
        order_id = order["OrderID"]
        items = order_items_lookup.get(order_id, [])

        calculated_subtotal = Decimal("0.00")

        for item in items:
            line_total = round_currency(
                Decimal(str(item["UnitPrice"]))
                * Decimal(str(item["Quantity"]))
            )
            calculated_subtotal += line_total

        calculated_subtotal = round_currency(calculated_subtotal)

        discount_rate = Decimal(str(order["DiscountRate"]))

        calculated_discount_amount = round_currency(
            calculated_subtotal * discount_rate
        )

        discounted_subtotal = (
            calculated_subtotal - calculated_discount_amount
        )

        shipping = Decimal(str(order["Shipping"]))

        calculated_tax = round_currency(
            (discounted_subtotal + shipping)
            * Decimal("0.07")
        )

        calculated_total = round_currency(
            discounted_subtotal
            + shipping
            + calculated_tax
        )

        order_total = Decimal(str(order["Total"]))

        if calculated_total != order_total:
            print()
            print("=" * 80)
            print("MISMATCHED ORDER FOUND")
            print(f"OrderID: {order_id}")
            print(f"Calculated Subtotal: {calculated_subtotal}")
            print(f"Stored Subtotal: {order['Subtotal']}")
            print(f"Discount Rate: {order['DiscountRate']}")
            print(f"Calculated Discount Amount: {calculated_discount_amount}")
            print(f"Stored Discount Amount: {order['DiscountAmount']}")
            print(f"Shipping: {order['Shipping']}")
            print(f"Calculated Tax: {calculated_tax}")
            print(f"Stored Tax: {order['Tax']}")
            print(f"Calculated Total: {calculated_total}")
            print(f"Stored Total: {order_total}")
            print("=" * 80)
            print()

            mismatched_orders.append(
                {
                    "OrderID": order_id,
                    "CalculatedTotal": calculated_total,
                    "OrderTotal": order_total,
                }
            )

    passed = len(mismatched_orders) == 0

    return {
        "name": "Order Totals Reconciled",
        "passed": passed,
        "records_checked": len(orders),
        "issues_found": len(mismatched_orders),
        "details": (
            f"{len(orders):,} orders checked. "
            f"{len(mismatched_orders):,} orders have mismatched totals."
        ),
    }
    

def validate_shipments_have_orders(shipments, orders):
    orders_lookup = build_orders_lookup(orders)
    shipments_without_orders = []
    
    for shipment in shipments:
        order_id = shipment["OrderID"]
        
        if order_id not in orders_lookup:
            shipments_without_orders.append(shipment)
    
    passed = len(shipments_without_orders) == 0
    
    return {
        "name": "Shipments Have Orders",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(shipments_without_orders),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(shipments_without_orders):,} shipments are missing orders."
        )
    }


def validate_shipments_have_successful_payments(shipments, payments):
    successful_payments_lookup = build_successful_payments_lookup(payments)
    shipments_without_successful_payments = []
    
    for shipment in shipments:
        order_id = shipment["OrderID"]
        
        if order_id not in successful_payments_lookup:
            shipments_without_successful_payments.append(shipment)
    
    passed = len(shipments_without_successful_payments) == 0
    
    return {
        "name": "Shipments Have Successful Payments",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(shipments_without_successful_payments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(shipments_without_successful_payments):,} shipments are missing successful payments."
        )
    }
    
    
def validate_shipment_dates_follow_payments(shipments, payments):
    successful_payments_lookup = build_successful_payments_lookup(payments)
    invalid_shipments = []
    
    for shipment in shipments:
        order_id = shipment["OrderID"]
        successful_payment = successful_payments_lookup.get(order_id)
        
        if successful_payment is None:
            continue
        
        payment_datetime = datetime.fromisoformat(
            successful_payment["PaymentDateTime"]
        )
        
        shipment_datetime = datetime.fromisoformat(
            shipment["ShipmentDateTime"]
        )
                       
        if shipment_datetime < payment_datetime:
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": order_id,
                    "PaymentDateTime": payment_datetime.isoformat(),
                    "ShipmentDateTime": shipment_datetime.isoformat(),
                }
            )
    
    passed = len(invalid_shipments) == 0
    
    return {
        "name": "Shipment Dates Follow Payments",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} shipments have invalid dates."
        )
    }


def validate_estimated_delivery_follows_shipment(shipments):
    invalid_shipments = []
    
    for shipment in shipments:
        shipment_datetime = datetime.fromisoformat(
            shipment["ShipmentDateTime"]
        )

        estimated_delivery_datetime = datetime.fromisoformat(
            shipment["EstimatedDeliveryDateTime"]
        )
        
        if estimated_delivery_datetime < shipment_datetime:
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": shipment["OrderID"],
                    "ShipmentDateTime": shipment_datetime.isoformat(),
                    "EstimatedDeliveryDateTime": estimated_delivery_datetime.isoformat(),
                }
            )
    
    passed = len(invalid_shipments) == 0
    
    return {
        "name": "Estimated Delivery Follows Shipment",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} shipments have invalid estimated delivery dates."
        )
    }
    
    
def validate_shipment_status_consistency(shipments):
    invalid_shipments = []

    for shipment in shipments:
        shipment_status = shipment["ShipmentStatus"]
        actual_delivery_datetime = shipment["ActualDeliveryDateTime"]

        if (
            shipment_status == "Delivered"
            and actual_delivery_datetime == ""
        ):
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": shipment["OrderID"],
                    "ShipmentStatus": shipment_status,
                    "ActualDeliveryDateTime": actual_delivery_datetime,
                }
            )

        elif (
            shipment_status != "Delivered"
            and actual_delivery_datetime != ""
        ):
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": shipment["OrderID"],
                    "ShipmentStatus": shipment_status,
                    "ActualDeliveryDateTime": actual_delivery_datetime,
                }
            )

    passed = len(invalid_shipments) == 0

    return {
        "name": "Shipment Status Consistency",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} shipments have inconsistent statuses."
        ),
    }
    
    
def validate_delayed_shipments(shipments):
    invalid_shipments = []

    for shipment in shipments:
        if shipment["IsDelayed"] != "True":
            continue

        shipment_status = shipment["ShipmentStatus"]
        actual_delivery_value = shipment["ActualDeliveryDateTime"]

        issue_details = {
            "ShipmentID": shipment["ShipmentID"],
            "OrderID": shipment["OrderID"],
            "ShipmentStatus": shipment_status,
            "IsDelayed": shipment["IsDelayed"],
            "EstimatedDeliveryDateTime": shipment[
                "EstimatedDeliveryDateTime"
            ],
            "ActualDeliveryDateTime": actual_delivery_value,
        }

        # A delayed shipment may still be traveling.
        if shipment_status == "In Transit":
            if actual_delivery_value != "":
                invalid_shipments.append(issue_details)

            continue

        # Any other delayed shipment must be Delivered.
        if shipment_status != "Delivered":
            invalid_shipments.append(issue_details)
            continue

        # Delivered shipments must have an actual delivery date.
        if actual_delivery_value == "":
            invalid_shipments.append(issue_details)
            continue

        estimated_delivery_datetime = datetime.fromisoformat(
            shipment["EstimatedDeliveryDateTime"]
        )

        actual_delivery_datetime = datetime.fromisoformat(
            actual_delivery_value
        )

        # A delayed delivery must arrive after its estimate.
        if actual_delivery_datetime <= estimated_delivery_datetime:
            invalid_shipments.append(issue_details)

    passed = len(invalid_shipments) == 0

    return {
        "name": "Delayed Shipments Are Valid",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} delayed shipments are invalid."
        ),
    }

    
def validate_non_delayed_shipments_valid(shipments):
    invalid_shipments = []

    for shipment in shipments:
        if shipment["IsDelayed"] != "False":
            continue

        shipment_status = shipment["ShipmentStatus"]
        actual_delivery_value = shipment["ActualDeliveryDateTime"]

        issue_details = {
            "ShipmentID": shipment["ShipmentID"],
            "OrderID": shipment["OrderID"],
            "ShipmentStatus": shipment_status,
            "IsDelayed": shipment["IsDelayed"],
            "EstimatedDeliveryDateTime": shipment[
                "EstimatedDeliveryDateTime"
            ],
            "ActualDeliveryDateTime": actual_delivery_value,
        }

        
        if shipment_status != "Delivered":   
            continue

        # Delivered shipments must have an actual delivery date.
        if actual_delivery_value == "":
            invalid_shipments.append(issue_details)
            continue

        estimated_delivery_datetime = datetime.fromisoformat(
            shipment["EstimatedDeliveryDateTime"]
        )

        actual_delivery_datetime = datetime.fromisoformat(
            actual_delivery_value
        )

        # A non-delayed delivery must arrive on or before its estimate.
        if actual_delivery_datetime > estimated_delivery_datetime:
            invalid_shipments.append(issue_details)

    passed = len(invalid_shipments) == 0

    return {
        "name": "Non-Delayed Shipments Are Valid",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} non-delayed shipments are invalid."
        ),
    }
  
  
def validate_shipping_cost_match_orders(shipments, orders):
    orders_lookup = build_orders_lookup(orders)
    mismatched_shipments = []

    for shipment in shipments:
        order_id = shipment["OrderID"]
        order = orders_lookup.get(order_id)

        if order is None:
            continue

        shipment_cost = float(shipment["ShippingCost"])
        order_shipping_cost = float(order["Shipping"])

        if round(shipment_cost, 2) != round(order_shipping_cost, 2):
            mismatched_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": order_id,
                    "ShipmentCost": shipment_cost,
                    "OrderShippingCost": order_shipping_cost,
                }
            )

    passed = len(mismatched_shipments) == 0

    return {
        "name": "Shipping Cost Matches Orders",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(mismatched_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(mismatched_shipments):,} shipments have mismatched shipping costs."
        ),
    }
  
  
  
def validate_carrier_tracking_present(shipments):
    invalid_shipments = []

    for shipment in shipments:
        carrier = shipment["Carrier"]
        tracking_number = shipment["TrackingNumber"]

        if carrier == "" or tracking_number == "":
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": shipment["OrderID"],
                    "Carrier": carrier,
                    "TrackingNumber": tracking_number
                }
            )

    passed = len(invalid_shipments) == 0

    return {
        "name": "Carrier and Tracking Number Present",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} shipments are missing carrier or tracking information."
        ),
    }
  
  
def validate_shipment_status_values(shipments):
    invalid_shipments = []

    valid_shipment_statuses = [
        "Processing",
        "In Transit",
        "Delivered",
        "Lost",
        "Damaged",
    ]

    for shipment in shipments:
        if shipment["ShipmentStatus"] not in valid_shipment_statuses:
            invalid_shipments.append(
                {
                    "ShipmentID": shipment["ShipmentID"],
                    "OrderID": shipment["OrderID"],
                    "ShipmentStatus": shipment["ShipmentStatus"],
                }
            )

    passed = len(invalid_shipments) == 0

    return {
        "name": "Shipment Status Values Are Valid",
        "passed": passed,
        "records_checked": len(shipments),
        "issues_found": len(invalid_shipments),
        "details": (
            f"{len(shipments):,} shipments checked. "
            f"{len(invalid_shipments):,} shipments have invalid status values."
        ),
    }
  
# ============================================================
# MAIN
# ============================================================

def main(
    customers_file,
    products_file,
    orders_file,
    order_items_file,
    payments_file,
    shipments_file=None
):

    customers = load_csv(customers_file)
    products = load_csv(products_file)
    orders = load_csv(orders_file)
    order_items = load_csv(order_items_file)
    payments = load_csv(payments_file)
    
    if shipments_file is not None:
        shipments = load_csv(shipments_file)
    
# ============================================================
# VALIDATIONS
# ============================================================
    
  
    
    results = []

    results.append(validate_orders_have_items(orders, order_items))
    results.append(validate_unique_order_ids(orders))
    results.append(validate_orders_have_payments(orders, payments))
    results.append(validate_order_items_have_products(order_items, products))
    results.append(validate_orders_have_customers(orders, customers))
    results.append(validate_payments_have_orders(payments, orders))
    results.append(validate_payment_amounts_match_order_totals(orders, payments))
    results.append(validate_order_totals_reconciled(orders, order_items))

    if shipments_file is not None:
        results.append(validate_shipments_have_orders(shipments, orders))
        results.append(
            validate_shipments_have_successful_payments(
                shipments,
                payments
            )
        )
        results.append(
            validate_shipment_dates_follow_payments(
                shipments,
                payments
            )
        )
        results.append(
            validate_estimated_delivery_follows_shipment(
                shipments
            )
        )
        results.append(
            validate_shipment_status_consistency(
                shipments
            )
        )
        results.append(
            validate_delayed_shipments(
                shipments
            )
        )
        results.append(
            validate_non_delayed_shipments_valid(
                shipments
            )
        )
        results.append(
            validate_shipping_cost_match_orders(
                shipments,
                orders
            )
        )
        results.append(
            validate_carrier_tracking_present(
                shipments
            )
        )
        results.append(
            validate_shipment_status_values(
                shipments
            )
        )
        
# ============================================================
# REPORTING
# ============================================================

    print("=" * REPORT_WIDTH)
    print("Northstar Commerce QA Report".center(REPORT_WIDTH))
    print("=" * REPORT_WIDTH)

    print("\nValidation Results")
    print("-" * REPORT_WIDTH)

    for index, result in enumerate(results):

        if index > 0:
            print("-" * REPORT_WIDTH)

        status = "PASS" if result["passed"] else "FAIL"
        symbol = "✓" if result["passed"] else "✗"

        print(f"{symbol} {result['name']:<40}{status}")
        print("-" * REPORT_WIDTH)
        print(f"   Records Checked : {result['records_checked']:,}")
        print(f"   Issues Found    : {result['issues_found']:,}")
        print(f"   {result['details']}")
        print()

    passed_count = sum(
        1 for result in results
        if result["passed"]
    )

    failed_count = len(results) - passed_count

    print()
    print("=" * REPORT_WIDTH)
    print("Summary".center(REPORT_WIDTH))
    print("=" * REPORT_WIDTH)
    print()

    print(f"Checks Passed          : {passed_count}")
    print(f"Checks Failed          : {failed_count}")
    print()

    overall_status = (
        "PASS"
        if failed_count == 0
        else "REVIEW REQUIRED"
    )

    certification_status = (
        "CERTIFIED FOR ANALYSIS"
        if failed_count == 0
        else "NOT CERTIFIED"
    )

    print(f"Overall Dataset Status : {overall_status}")

    print()
    print("=" * REPORT_WIDTH)
    print("Dataset Quality Certification".center(REPORT_WIDTH))
    print("=" * REPORT_WIDTH)
    print()

    if failed_count == 0:
        print("✓ Referential Integrity Verified")
        print("✓ Financial Integrity Verified")
        print("✓ Timeline Integrity Verified")
        print("✓ Business Rules Verified")
        print("✓ Shipment Lifecycle Verified")
        print("✓ Data Quality Verified")
    else:
        print("✗ One or more validation checks require review.")

    print()
    print(f"Dataset Certification  : {certification_status}")
    print("QA Framework Version   : 1.0")
    print()

    print("Approved For Downstream Analytics:")

    if failed_count == 0:
        print("✓ SQL Analysis")
        print("✓ Power BI Reporting")
        print()
        print("=" * REPORT_WIDTH)
        print("End of QA Report".center(REPORT_WIDTH))
        print("=" * REPORT_WIDTH)
    else:
        print("✗ SQL Analysis")
        print("✗ Power BI Reporting")
        print()
        print("=" * REPORT_WIDTH)
        print("End of QA Report".center(REPORT_WIDTH))
        print("=" * REPORT_WIDTH)
        
if __name__ == "__main__":

    if DATASET == "operational":
        main(
            CUSTOMERS_FILE,
            PRODUCTS_FILE,
            ORDERS_FILE,
            ORDER_ITEMS_FILE,
            PAYMENTS_FILE,
            SHIPMENTS_FILE,
        )

    elif DATASET == "training":
        main(
            TRAINING_CUSTOMERS_FILE,
            TRAINING_PRODUCTS_FILE,
            TRAINING_ORDERS_FILE,
            TRAINING_ORDER_ITEMS_FILE,
            TRAINING_PAYMENTS_FILE,
        )

    else:
        raise ValueError(
            f"Unknown dataset: {DATASET}"
        )