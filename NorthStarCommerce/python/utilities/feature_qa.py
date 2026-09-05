"""
===============================================================================
Project NorthStar
Feature QA Engine
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-24
Version: 1.0

Purpose:
Validate NorthStar feature calculations and certify the final assembled
customer feature dataset before it is approved for downstream use.

Business Objective:
Ensure that engineered business evidence is mathematically correct,
structurally complete, and consistent with NorthStar business rules before
being written to output or supplied to machine learning systems.

Core Responsibilities:
- Validate individual feature calculations using controlled test scenarios.
- Validate business rules governing feature generation.
- Validate the structure of the assembled feature dataset.
- Detect duplicate or missing customer keys.
- Confirm all required feature columns are present.
- Reconcile the final feature population against the expected business
  population.
- Produce standardized PASS/FAIL QA results.
- Provide diagnostic information that identifies the source of validation
  failures.

Current Feature QA:
- Purchase Interval Standard Deviation
- Average Interval Change
- Purchase Frequency
- Successful Purchase History
- Purchase History As-Of
- Historical Feature Dataset

Feature Dataset Certification:
- Duplicate customer key validation
- Missing customer key validation
- Required feature column validation
- Customer population reconciliation

QA Result Contract:
Each validation returns a standardized result containing:

    name
    passed
    records_checked
    issues_found
    details

Diagnostic Principle:
QA should not only detect failure; it should provide enough information to
identify where investigation should begin.

Certification Policy:
The Feature QA Engine determines whether the assembled feature dataset satisfies
NorthStar's required quality rules. Final output authorization is enforced by
the Feature Pipeline Runner.

Engineering Principles:
- Business rules must be testable.
- Controlled scenarios should have known expected outcomes.
- QA logic remains separate from feature-generation logic.
- Validation should fail clearly and provide useful diagnostic information.
- Missing or invalid evidence must not be silently treated as valid.
- QA results should follow a consistent reporting structure.
- Prefer the simplest design that remains clear, maintainable, and teachable.

Future Expansion:
This engine is designed to support QA for additional feature families,
historical observation features, and future NorthStar business features
without expanding beyond the Feature Engineering layer.
===============================================================================
"""
import pandas as pd

from generators.feature_engineering import (
    generate_purchase_interval_stddev,
    generate_average_interval_change,
    generate_purchase_history_as_of,
    generate_purchase_features,
    generate_successful_purchase_history,
    build_feature_dataset,
)

# =====================================================================
# Feature QA
# =====================================================================

def validate_purchase_interval_stddev():
    issues = []
    
    # Perfect consistency
    purchase_intervals = pd.Series([30, 30, 30, 30, 30, 30, 30, 30, 30, 30])
    actual_result = generate_purchase_interval_stddev(purchase_intervals)
    if actual_result != 0:
        issues.append("Perfect consistency scenario failed.")

    # Variable behavior
    purchase_intervals = pd.Series([30, 31, 29, 30, 27, 33, 15, 44, 30, 28])
    actual_result = generate_purchase_interval_stddev(purchase_intervals)
    if actual_result <= 0:
        issues.append("Variable consistency scenario failed.")
        
    # Insufficient history - 9 intervals
    purchase_intervals = pd.Series(
        [30, 31, 29, 30, 27, 33, 15, 44, 30]
    )
    actual_result = generate_purchase_interval_stddev(purchase_intervals)

    if not pd.isna(actual_result):
        issues.append(
            "Nine purchase intervals should be insufficient history."
        )


    # Minimum reliable history - 10 intervals
    purchase_intervals = pd.Series(
        [30, 31, 29, 30, 27, 33, 15, 44, 30, 28]
    )
    actual_result = generate_purchase_interval_stddev(purchase_intervals)

    if pd.isna(actual_result):
        issues.append(
            "Ten purchase intervals should meet reliable history."
        )        
        
    passed = len(issues) == 0
    
    return {
        "name": "Purchase Interval StdDev",
        "passed": passed,
        "records_checked": 4,
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }


def validate_average_interval_change():
    
    issues = []
    
    # Intervals Spread
    average_interval_change = pd.DataFrame({
        "DaysBetweenPurchases": [
            30, 35, 40, 45, 50,
            55, 60, 65, 70, 75
        ],
        "PurchaseIntervalChange": [
            pd.NA, 5, 5, 5, 5,
            5, 5, 5, 5, 5
        ],
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if actual_result != 5:
        issues.append("Intervals spread scenario failed.")
       
        
    # Intervals Shrink
    average_interval_change = pd.DataFrame({
        "DaysBetweenPurchases": [
            75, 70, 65, 60, 55,
            50, 45, 40, 35, 30
        ],
        "PurchaseIntervalChange": [
            pd.NA, -5, -5, -5, -5,
            -5, -5, -5, -5, -5
        ],
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if actual_result != -5:
        issues.append("Intervals shrink scenario failed.")
        
        
    # Stable interval
    average_interval_change = pd.DataFrame({
        "DaysBetweenPurchases": [
            30, 30, 30, 30, 30,
            30, 30, 30, 30, 30
        ],
        "PurchaseIntervalChange": [
            pd.NA, 0, 0, 0, 0,
            0, 0, 0, 0, 0
        ],
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if actual_result != 0:
        issues.append("Stable interval scenario failed.")
    
    
    # Insufficient history
    average_interval_change = pd.DataFrame({
        "DaysBetweenPurchases": [
            30, 35, 40, 45, 50,
            55, 60, 65, 70
        ],
        "PurchaseIntervalChange": [
            pd.NA, 5, 5, 5, 5,
            5, 5, 5, 5
        ],
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if not pd.isna(actual_result):
        issues.append("Insufficient history scenario failed.")   
        
    passed = len(issues) == 0
    
    return {
        "name": "Average Interval Change",
        "passed": passed,
        "records_checked": 4,
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }
         
         
def validate_purchase_frequency():
    issues = []

    purchase_history = pd.DataFrame({
        "AnonymousCustomerKey": [
            "SinglePurchaseCustomer",
            "RepeatPurchaseCustomer",
        ],
        "OrderDateTime": pd.to_datetime([
            "2026-01-01",
            "2026-01-01",
        ]),
        "Total": [
            50.00,
            50.00,
        ],
    })

    repeat_purchase = pd.DataFrame({
        "AnonymousCustomerKey": [
            "RepeatPurchaseCustomer",
        ],
        "OrderDateTime": pd.to_datetime([
            "2026-01-11",
        ]),
        "Total": [
            75.00,
        ],
    })

    purchase_history = pd.concat(
        [
            purchase_history,
            repeat_purchase,
        ],
        ignore_index=True,
    )

    purchase_features = generate_purchase_features(
        purchase_history
    )

    single_purchase_frequency = purchase_features.loc[
        purchase_features["AnonymousCustomerKey"] == "SinglePurchaseCustomer",
        "PurchaseFrequency",
    ].iloc[0]

    if not pd.isna(single_purchase_frequency):
        issues.append(
            "Single-purchase customer should have missing PurchaseFrequency."
        )

    passed = len(issues) == 0

    return {
        "name": "Purchase Frequency",
        "passed": passed,
        "records_checked": 1,
        "issues_found": len(issues),
        "details": " | ".join(issues),
    }
    
         
def validate_feature_dataset(
    feature_dataset, 
    successful_purchase_history
):
    
    issues = []
    
    required_columns = [
        "AnonymousCustomerKey",
        "DaysSinceLastPurchase",
        "AverageDaysBetweenPurchases",
        "SuccessfulOrderCount",
        "AverageOrderValue",
        "PurchaseFrequency",
        "PurchaseIntervalStdDev",
        "AverageIntervalChange"
    ]
    
    # Unique customer keys
    if feature_dataset["AnonymousCustomerKey"].duplicated().any():
        issues.append("Duplicate customer keys found.")
    
    
    # Missing customer keys
    if feature_dataset["AnonymousCustomerKey"].isna().any():
        issues.append("Customer key missing.")
    
    
    # Required feature columns
    for column in required_columns:
        if column not in feature_dataset.columns:
            issues.append(f"Missing required column: {column}")
    
    # Population reconciliation
    expected_customer_count = len(
        successful_purchase_history["AnonymousCustomerKey"].unique()
    )
    
    actual_customer_count = len(feature_dataset)
    
    if expected_customer_count != actual_customer_count:
        issues.append(
            f"Customer population mismatch: "
            f"expected {expected_customer_count}, "
            f"found {actual_customer_count}."      
    )
    
    passed = len(issues) == 0
    
    return {
        "name": "Feature Dataset",
        "passed": passed,
        "records_checked": len(feature_dataset),
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }


def validate_successful_purchase_history():
    issues = []

    orders_df = pd.DataFrame({
        "AnonymousOrderKey": [
            "ORDER_A",
            "ORDER_B",
        ],
        "AnonymousCustomerKey": [
            "CUSTOMER_A",
            "CUSTOMER_B",
        ],
        "OrderDateTime": [
            "2026-01-01 10:00:00",
            "2026-01-02 10:00:00",
        ],
        "Total": [
            50.00,
            75.00,
        ],
    })

    payments_df = pd.DataFrame({
        "AnonymousOrderKey": [
            "ORDER_A",
            "ORDER_A",
            "ORDER_B",
        ],
        "PaymentStatus": [
            "Successful",
            "Successful",
            "Failed",
        ],
    })

    actual_result = generate_successful_purchase_history(
        orders_df,
        payments_df,
    )

    if len(actual_result) != 1:
        issues.append(
            "Successful purchase history row count validation failed."
        )

    if actual_result["AnonymousOrderKey"].duplicated().any():
        issues.append(
            "Duplicate successful purchase found."
        )

    passed = len(issues) == 0

    return {
        "name": "Successful Purchase History",
        "passed": passed,
        "records_checked": len(actual_result),
        "issues_found": len(issues),
        "details": " | ".join(issues),
    }

    
def validate_purchase_history_as_of():
    
    issues = []
    
    successful_purchase_history = pd.DataFrame({
        "AnonymousCustomerKey": [
            "Customer_A",
            "Customer_A",
            "Customer_A",
        ],
        
        "OrderDateTime": [
            "2025-05-01",
            "2025-05-20",
            "2025-06-10",
        ]
    })
    
    successful_purchase_history["OrderDateTime"] = pd.to_datetime(
        successful_purchase_history["OrderDateTime"]
    )
    
    observation_date = pd.to_datetime("2025-06-01")
    
    actual_result = generate_purchase_history_as_of(
        successful_purchase_history,
        observation_date,
    )
    
    if len(actual_result) != 2:
        issues.append("Purchase history as-of row count scenario failed.")
        
    if (actual_result["OrderDateTime"] > observation_date).any():
        issues.append("Observation date check failed")
        
    passed = len(issues) == 0
    
    return {
        "name": f"Purchase History as of {observation_date}",
        "passed": passed,
        "records_checked": 3,
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }
    
      
def validate_historical_feature_dataset():
    
    issues = []
    
    observation_date = pd.to_datetime("2025-06-01")
    
    feature_dataset, qa_purchase_history = build_feature_dataset(
        observation_date
    )
    
    if feature_dataset.empty:
        issues.append("Historical feature dataset is empty")
        
    if (qa_purchase_history["OrderDateTime"] > observation_date).any():
        issues.append("Observation Date check failed")        
        
    
    
    feature_dataset_qa = validate_feature_dataset(
        feature_dataset,
        qa_purchase_history,
    )
    
    if not feature_dataset_qa["passed"]:
        issues.append(
            f"Historical feature dataset reconciliation failed: "
            f"{feature_dataset_qa['details']}"
        )
        
    passed = len(issues) == 0
    
    return {
        "name": f"Historical Feature Dataset as of {observation_date}",
        "passed": passed,
        "records_checked": len(feature_dataset),
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }
       
# =====================================================================
# Main
# =====================================================================
    
def main():

    # Controlled Feature QA
    standard_deviation = validate_purchase_interval_stddev()

    average_interval_change = validate_average_interval_change()
    
    purchase_frequency = validate_purchase_frequency()
    
    successful_purchase_history_qa = validate_successful_purchase_history()

    # Build Real Feature Dataset
    feature_dataset, successful_purchase_history = build_feature_dataset()

    # Feature Dataset Assembly QA
    feature_dataset_qa = validate_feature_dataset(
        feature_dataset,
        successful_purchase_history,
    )

    purchase_history_as_of = validate_purchase_history_as_of()

    historical_feature_dataset = validate_historical_feature_dataset()


if __name__ == "__main__":
    main()