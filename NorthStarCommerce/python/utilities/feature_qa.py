
import pandas as pd

from generators.feature_engineering import (
    generate_purchase_interval_stddev,
    generate_average_interval_change,
    build_feature_dataset,
)


# =====================================================================
# Feature QA Helper
# =====================================================================



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
        
    # Insufficient history
    purchase_intervals = pd.Series([], dtype="float64")
    actual_result = generate_purchase_interval_stddev(purchase_intervals)
    if not pd.isna(actual_result):
        issues.append("Insufficient history scenario failed.")
        
    # Non - negative results
    # purchase_intervals = pd.Series([30, 31, 29, 30])
    # actual_result = generate_purchase_interval_stddev(purchase_intervals)
    # if actual_result < 0:
    #     issues.append("Negative standard deviation scenario failed.")
        
        
    passed = len(issues) == 0
    
    return {
        "name": "Purchase Interval StdDev",
        "passed": passed,
        "records_checked": 3,
        "issues_found": len(issues),
        "details": " | ".join(issues)
    }




def validate_average_interval_change():
    
    issues = []
    
    # Intervals Spread
    average_interval_change = pd.DataFrame({
        "PurchaseIntervalChange":[pd.NA, pd.NA, 5, 5, 5, 5, 5, 5, 5, 5]
    })
    
    acutal_result = generate_average_interval_change(
        average_interval_change
    )
    
    if acutal_result != 5:
        issues.append("Intervals spread scenario failed.")
       
        
    # Intervals Shrink
    average_interval_change = pd.DataFrame({
        "PurchaseIntervalChange": [pd.NA, pd.NA, -5, -5, -5, -5, -5, -5, -5, -5]
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if actual_result != -5:
        issues.append("Intervals shrink scenario failed.")
        
        
    # Stable interval
    average_interval_change = pd.DataFrame({
        "PurchaseIntervalChange": [pd.NA, pd.NA, 0, 0, 0, 0, 0, 0, 0, 0]
    })
    
    actual_result = generate_average_interval_change(
        average_interval_change
    )
    
    if actual_result != 0:
        issues.append("Stable interval scenario failed.")
    
    
    # Insufficient history
    average_interval_change = pd.DataFrame({
        "PurchaseIntervalChange": [],
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
    
# =====================================================================
# Main
# =====================================================================
    
def main():

    # Controlled Feature QA
    standard_deviation = validate_purchase_interval_stddev()
    print(standard_deviation)

    average_interval_change = validate_average_interval_change()
    print(average_interval_change)

    # Build Real Feature Dataset
    feature_dataset, successful_purchase_history = build_feature_dataset()

    # Feature Dataset Assembly QA
    feature_dataset_qa = validate_feature_dataset(
        feature_dataset,
        successful_purchase_history,
    )

    print(feature_dataset_qa)


if __name__ == "__main__":
    main()