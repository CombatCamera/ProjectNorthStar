"""
===============================================================================
Project NorthStar
Business Interpretation QA
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-26
Version: 1.0

Purpose:
Validate NorthStar's Business Interpretation Engine using controlled test cases
with known expected business outcomes.

Version 1.0 Scope:
Customer Purchase Health

Validation Objectives:
- Verify Healthy Window calculations.
- Verify Percent Beyond Healthy Window calculations.
- Verify Purchase Health Score calculations.
- Verify Purchase Health Tier classifications.
- Verify insufficient-history handling.
- Verify Purchase Health Score remains within the 0-100 range.

QA Principle:
Business interpretation must be validated against known business rules before
its output may be consumed by downstream analytics or machine learning.
===============================================================================
"""

import pandas as pd

from Interpretation.business_interpretation import (
    generate_purchase_health,
)

# ==================================================
# Functions
# ==================================================

def validate_purchase_health():

    issues = []
    
    test_features = pd.DataFrame({
        "AnonymousCustomerKey": [
            "HealthyCustomer",
            "WatchCustomer",
            "AtRiskCustomer",
            "CriticalCustomer",
            "InsufficientHistoryCustomer",
        ],
        "DaysSinceLastPurchase": [
            10, 
            14,
            16,
            18,
            20,
            
        ],
        "AverageDaysBetweenPurchases": [
            10, 
            10,
            10,
            10,
            pd.NA,
        ],
    })
    
    purchase_health = generate_purchase_health(
        test_features
    )
    
    purchase_health.loc[0, "PurchaseHealthTier"]
    
    if purchase_health.loc[0, "PurchaseHealthTier"] != "Healthy":
        issues.append("Healthy customer classification failed.")
        
    if purchase_health.loc[1, "PurchaseHealthTier"] != "Watch":
        issues.append("Watch customer classification failed.")
        
    if purchase_health.loc[2, "PurchaseHealthTier"] != "At Risk":
        issues.append("At Risk customer classification failed.")
        
    if purchase_health.loc[3, "PurchaseHealthTier"] != "Critical":
        issues.append("Critical customer classification failed.")
        
    if purchase_health.loc[4, "PurchaseHealthTier"] != "Insufficient History":
        issues.append("Insufficient History classification failed.")
        
    valid_purchase_health_scores = purchase_health[
        "PurchaseHealthScore"
    ].dropna()

    if not valid_purchase_health_scores.between(0, 100).all():
        issues.append("Purchase Health Score boundary validation failed.")
        
    passed = len(issues) == 0
    
    return {
        "name": "Purchase Health Interpretation",
        "passed": passed,
        "records_checked": len(test_features),
        "issues_found": len(issues),
        "details": " | ".join(issues),
    }

# ==================================================
# Main
# ==================================================

def main():
    
    purchase_health = validate_purchase_health()
    print(purchase_health)
    
if __name__ == "__main__":
    main() 