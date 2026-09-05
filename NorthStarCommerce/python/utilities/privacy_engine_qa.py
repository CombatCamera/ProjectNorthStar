
"""
===============================================================================
Project NorthStar
Engine: Privacy Engine QA
File: privacy_engine_qa.py
Author: Mat Thompson
Version: 1.0
Last Updated: 2026-09-05

Purpose:
    Validate the Privacy Engine's controlled privacy transformations
    and supporting business rules.

Responsibilities:
    - Validate temporal offset boundary calculations.
    - Verify temporal offset calculations preserve required date constraints.
    - Provide controlled QA tests for Privacy Engine behavior.

Design Principle:
    Privacy transformations must protect customer identity while
    preserving the behavioral relationships required for downstream
    analytics and machine learning.
===============================================================================
"""


from datetime import datetime, timedelta
from utilities.privacy_engine import (
    calculate_maximum_safe_offset,
    MAX_TEMPORAL_OFFSET_DAYS,
)

# ================================================================
# FUNCTIONS
# ================================================================

# Validation Function for Temporal Offset Mapping
def validate_maximum_safe_offset():
    today = datetime.now()

    recent_event_date = today - timedelta(days=5)
    older_event_date = today - timedelta(days=200)
    very_old_event_date = today - timedelta(days=500)

    recent_maximum_offset = calculate_maximum_safe_offset(
        today,
        recent_event_date,
    )

    older_maximum_offset = calculate_maximum_safe_offset(
        today,
        older_event_date,
    )

    very_old_maximum_offset = calculate_maximum_safe_offset(
        today,
        very_old_event_date,
    )

    assert recent_maximum_offset == 5
    assert older_maximum_offset == 200
    assert very_old_maximum_offset == MAX_TEMPORAL_OFFSET_DAYS

    print("✓ Maximum safe temporal offset validated")
    
# ================================================================
# MAIN
# ================================================================
def main():
    
    validate_maximum_safe_offset()

if __name__ == "__main__":
    main()