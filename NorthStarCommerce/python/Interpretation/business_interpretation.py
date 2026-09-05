"""
===============================================================================
Project NorthStar
Business Interpretation Engine
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-26
Version: 1.0

Purpose:
Interpret reusable business evidence produced by NorthStar Feature Engineering
and convert that evidence into standardized business states and classifications.

Business Objective:
Provide a single, reusable source of business truth that downstream analytics,
machine learning, reporting, and operational systems can consume consistently.

Core Responsibilities:
- Consume QA-certified business features.
- Apply documented business interpretation rules.
- Generate standardized business states and classifications.
- Preserve separation between evidence generation and business interpretation.
- Provide canonical business truth for downstream systems.

Version 1.0 Scope:
Customer Purchase Health

Purchase Health Interpretation:
- Healthy Window
- Percent Beyond Healthy Window
- Purchase Health Score
- Purchase Health Tier

Purchase Health Tiers:
- Healthy
- Watch
- At Risk
- Critical
- Insufficient History

Engineering Principles:
- Feature Engineering creates evidence.
- Business Interpretation determines what the evidence means.
- Business rules must have one canonical implementation.
- Machine learning consumes business truth; it does not define it.
- Interpretation logic must remain reusable outside machine learning.
- Prefer the simplest design that remains clear, maintainable, and teachable.

Machine Learning Principle:
The Business Interpretation Engine acts as the teacher by establishing the
business truth that predictive models learn to anticipate.

Future Expansion:
This engine is designed to support additional business interpretations without
coupling those interpretations to Feature Engineering or machine learning.
===============================================================================
"""


import pandas as pd
from generators.feature_engineering import (
    build_feature_dataset,
)

def generate_purchase_health(feature_dataset):
    
    purchase_health = feature_dataset.copy()
    
    purchase_health["HealthyWindowDays"] = (
        purchase_health["AverageDaysBetweenPurchases"] * 1.20
    )
    
    purchase_health["PercentBeyondHealthyWindow"] = pd.NA
    
    valid_health_history = (
        purchase_health["HealthyWindowDays"].notna()
        & (purchase_health["HealthyWindowDays"] > 0)
    )

    within_healthy_window = pd.Series(
        False,
        index=purchase_health.index,
    )

    within_healthy_window.loc[valid_health_history] = (
        purchase_health.loc[
            valid_health_history,
            "DaysSinceLastPurchase"
        ]
        <=
        purchase_health.loc[
            valid_health_history,
            "HealthyWindowDays"
        ]
    )

    beyond_healthy_window = (
        valid_health_history
        & ~within_healthy_window
    )

    # Percent Beyond Healthy Window
    purchase_health.loc[
        within_healthy_window,
        "PercentBeyondHealthyWindow"
    ] = 0

    purchase_health.loc[
        beyond_healthy_window,
        "PercentBeyondHealthyWindow"
    ] = (
        (
            purchase_health.loc[
                beyond_healthy_window,
                "DaysSinceLastPurchase"
            ]
            -
            purchase_health.loc[
                beyond_healthy_window,
                "HealthyWindowDays"
            ]
        )
        /
        purchase_health.loc[
            beyond_healthy_window,
            "HealthyWindowDays"
        ]
    )

    # Purchase Health Score
    purchase_health["PurchaseHealthScore"] = pd.NA

    purchase_health.loc[
        within_healthy_window,
        "PurchaseHealthScore"
    ] = 100

    purchase_health.loc[
        beyond_healthy_window,
        "PurchaseHealthScore"
    ] = (
        100
        -
        (
            purchase_health.loc[
                beyond_healthy_window,
                "PercentBeyondHealthyWindow"
            ]
            * 100
        )
    )

    # Floor Purchase Health Score at 0
    purchase_health.loc[
        purchase_health["PurchaseHealthScore"].notna()
        & (purchase_health["PurchaseHealthScore"] < 0),
        "PurchaseHealthScore"
    ] = 0
    

    # Purchase Health Tier
    purchase_health["PurchaseHealthTier"] = "Insufficient History"
    
    purchase_health.loc[
        purchase_health["PurchaseHealthScore"] >= 95,
        "PurchaseHealthTier"
    ] = "Healthy"
    
    purchase_health.loc[
        (
            purchase_health["PurchaseHealthScore"] >= 80
        )
        & (
            purchase_health["PurchaseHealthScore"] < 95
        ),
        "PurchaseHealthTier"
    ] = "Watch"
    
    purchase_health.loc[
        (
            purchase_health["PurchaseHealthScore"] >= 60
        )
        & (
            purchase_health["PurchaseHealthScore"] < 80
        ),
        "PurchaseHealthTier"
    ] = "At Risk"
        
    purchase_health.loc[
        (
            purchase_health["PurchaseHealthScore"] >= 0
        )
        & (
            purchase_health["PurchaseHealthScore"] < 60
        ),
        "PurchaseHealthTier"
    ] = "Critical"
    
    return purchase_health

# ========================================
# MAIN
# ========================================
def main():

    feature_dataset, _ = build_feature_dataset()

    purchase_health = generate_purchase_health(
        feature_dataset
    )

    print(purchase_health.head())
    print(purchase_health.shape)
    print(purchase_health["PurchaseHealthTier"].value_counts(dropna=False))
    
    
    
if __name__ == "__main__":
    main()