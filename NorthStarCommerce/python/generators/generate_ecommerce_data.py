"""
===============================================================================
Project:        Project NorthStar
Engine:         NorthStar Commerce Generation Engine
File:           generate_ecommerce_data.py
Author:         Mat Thompson
Created:        2026-07-25
Last Updated:   2026-08-17
Version:        2.0

Purpose:
    Generate a realistic synthetic e-commerce enterprise dataset for SQL,
    business intelligence, analytics, and machine learning practice.
    This engine serves as the single source of truth for NorthStar Commerce
    data generation.

Inputs:
    - Configuration constants
    - Business rules
    - Probability distributions

Outputs:
    - customers.csv
    - categories.csv
    - products.csv
    - orders.csv
    - order_items.csv
    - payments.csv
    - shipments.csv

Current Responsibilities:
    - Generate realistic customer populations.
    - Generate product catalog and categories.
    - Generate realistic purchasing behavior.
    - Generate order items and financial totals.
    - Generate payment histories.
    - Generate shipment histories.
    - Export enterprise datasets.

Non-Responsibilities:
    - Data quality validation
    - Privacy protection
    - Data standardization
    - Feature engineering
    - Machine learning
    - Predictive analytics

Engineering Laws:
    1. Business realism over random data.
    2. Every function has one responsibility.
    3. Shared business rules have one source of truth.
    4. Generate data once; reuse it many times.

Future Architecture:
    Shared Generation Engine
            │
            ├── Operational Commerce Dataset
            └── Training Population Dataset

===============================================================================
"""


import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# ============================================================
# GENERATOR SETTINGS
# ============================================================

RANDOM_SEED = 42

START_DATE = date(2023, 1, 1)
END_DATE = date.today()

CURRENT_DATETIME = datetime.combine(
    END_DATE,
    datetime.max.time()
)

NUMBER_OF_CUSTOMERS = 5_000
NUMBER_OF_PRODUCTS = 120

CURRENCY_PRECISION = Decimal("0.01")


random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT FILES
# ============================================================

CUSTOMERS_FILE = RAW_DATA_FOLDER / "customers.csv"
CATEGORIES_FILE = RAW_DATA_FOLDER / "categories.csv"
PRODUCTS_FILE = RAW_DATA_FOLDER / "products.csv"
ORDERS_FILE = RAW_DATA_FOLDER / "orders.csv"
ORDER_ITEMS_FILE = RAW_DATA_FOLDER / "order_items.csv"
PAYMENTS_FILE = RAW_DATA_FOLDER / "payments.csv"
SHIPMENTS_FILE = RAW_DATA_FOLDER / "shipments.csv"

# Reserved for future returns module.
RETURNS_FILE = RAW_DATA_FOLDER / "returns.csv"


# ============================================================
# PRODUCT CONFIGURATION
# ============================================================

CATEGORY_PROFILES = {
    "Electronics": {
        "adjectives": ["Essential", "Advanced", "Compact", "Wireless", "Premium"],
        "nouns": ["Headphones", "Speaker", "Charger"],
        "price_range": (25.00, 250.00),
    },
    "Home & Kitchen": {
        "adjectives": ["Classic", "Modern", "Deluxe", "Compact", "Professional"],
        "nouns": ["Cookware Set", "Coffee Maker", "Blender"],
        "price_range": (20.00, 300.00),
    },
    "Office": {
        "adjectives": ["Ergonomic", "Executive", "Essential", "Compact", "Premium"],
        "nouns": ["Desk Chair", "Desk Lamp", "Organizer"],
        "price_range": (15.00, 350.00),
    },
    "Fitness": {
        "adjectives": ["Performance", "Adjustable", "Portable", "Essential", "Professional"],
        "nouns": ["Dumbbell Set", "Yoga Mat", "Resistance Kit"],
        "price_range": (15.00, 275.00),
    },
    "Outdoor": {
        "adjectives": ["Trail", "Weatherproof", "Adventure", "Lightweight", "Expedition"],
        "nouns": ["Backpack", "Camping Chair", "Cooler"],
        "price_range": (25.00, 325.00),
    },
    "Beauty & Personal Care": {
        "adjectives": ["Daily", "Radiant", "Essential", "Premium", "Refreshing"],
        "nouns": ["Skin Care Set", "Hair Dryer", "Grooming Kit"],
        "price_range": (15.00, 180.00),
    },
    "Pet Supplies": {
        "adjectives": ["Comfort", "Durable", "Interactive", "Travel", "Premium"],
        "nouns": ["Pet Bed", "Feeding Set", "Toy Pack"],
        "price_range": (10.00, 160.00),
    },
    "Toys & Games": {
        "adjectives": ["Creative", "Family", "Classic", "Educational", "Adventure"],
        "nouns": ["Board Game", "Building Set", "Activity Kit"],
        "price_range": (10.00, 140.00),
    },
}


PRICE_TIER_PROFILES = {
    "low": {
        "quantities": [1, 2, 3, 4, 5],
        "weights": [45, 30, 15, 7, 3]
    },

    "medium": {
        "quantities": [1, 2, 3],
        "weights": [70, 20, 10]
    },

    "high": {
        "quantities": [1, 2],
        "weights": [95, 5]
    },

    "premium": {
        "quantities": [1],
        "weights": [100]
    }
}

# ============================================================
# CUSTOMER CONFIGURATION
# ============================================================

MALE_FIRST_NAMES = [
    "James", "Robert", "John", "Michael", "David",
    "William", "Richard", "Joseph", "Thomas", "Christopher",
    "Daniel", "Matthew", "Anthony", "Mark", "Donald",
    "Andrew", "Joshua", "Kevin", "Brian", "George",
    "Charles", "Steven", "Edward", "Paul", "Jason",
    "Ryan", "Jacob", "Justin", "Brandon", "Nathan",
]

FEMALE_FIRST_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Emily", "Ashley", "Amanda", "Melissa", "Stephanie",
    "Lauren", "Rachel", "Nicole", "Megan", "Rebecca",
    "Christina", "Olivia", "Emma", "Sophia", "Abigail",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris",
    "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Flores",
]

LOCATION_PROFILES = {
    "Northeast": [
        ("Boston", "MA"),
        ("New York", "NY"),
        ("Philadelphia", "PA"),
        ("Buffalo", "NY"),
        ("Pittsburgh", "PA"),
        ("Providence", "RI"),
        ("Hartford", "CT"),
        ("Newark", "NJ"),
    ],
    "South": [
        ("Atlanta", "GA"),
        ("Charlotte", "NC"),
        ("Nashville", "TN"),
        ("Dallas", "TX"),
        ("Houston", "TX"),
        ("Miami", "FL"),
        ("Orlando", "FL"),
        ("Richmond", "VA"),
    ],
    "Midwest": [
        ("Chicago", "IL"),
        ("Detroit", "MI"),
        ("Columbus", "OH"),
        ("Cleveland", "OH"),
        ("Indianapolis", "IN"),
        ("Milwaukee", "WI"),
        ("Minneapolis", "MN"),
        ("St. Louis", "MO"),
    ],
    "West": [
        ("Los Angeles", "CA"),
        ("San Diego", "CA"),
        ("San Francisco", "CA"),
        ("Seattle", "WA"),
        ("Portland", "OR"),
        ("Denver", "CO"),
        ("Phoenix", "AZ"),
        ("Las Vegas", "NV"),
    ],
}

REGION_WEIGHTS = {
    "Northeast": 18,
    "South": 37,
    "Midwest": 21,
    "West": 24,
}

CUSTOMER_SEGMENT_WEIGHTS = {
    "Consumer": 72,
    "Small Business": 22,
    "Enterprise": 6,
}

SHOPPING_PROFILE_WEIGHTS = {
    "Occasional": 35,
    "Regular": 40,
    "Frequent": 20,
    "VIP": 5,
}

SHOPPING_PROFILE_ORDER_RANGES = {
    "Occasional": (1, 3),
    "Regular": (4, 8),
    "Frequent": (9, 18),
    "VIP": (19, 35),
}

LOYALTY_TIER_WEIGHTS = {
    "Bronze": 60,
    "Silver": 25,
    "Gold": 12,
    "Platinum": 3,
}

EMAIL_DOMAINS = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
    "protonmail.com",
]

#=============================================================
# BUSINESS CONFIGURATION
#=============================================================

#=ORDER TIMING================================================

ORDER_HOURS = list(range(24))

ORDER_HOUR_WEIGHTS = [
    1, 1, 1, 1, 1, 2,       # 12 AM–5 AM
    3, 4, 5,                # 6 AM–8 AM
    7, 8, 9, 9, 9, 9, 8, 8,  # 9 AM–4 PM
    11, 13, 14, 13, 11,     # 5 PM–9 PM
    6, 3                    # 10 PM–11 PM
]

#=SHIPPING====================================================

SHIPPING_METHODS = ["Standard", "Two-Day", "Next-Day"]
SHIPPING_METHOD_WEIGHTS = [80, 15, 5]

SHIPPING_RATES = {
    "Standard": Decimal("5.99"),
    "Two-Day": Decimal("12.99"),
    "Next-Day": Decimal("24.99"),
}

FREE_SHIPPING_THRESHOLD = Decimal("125.00")

SHIPPING_PROCESSING_HOURS = {
        "Standard": (12, 48),
        "Two-Day": (6, 24),
        "Next-Day": (2, 12),
    }

SHIPPING_TRANSIT_DAYS = {
    "Standard": (3, 7),
    "Two-Day": (2, 2),
    "Next-Day": (1, 1),
}

SHIPPING_CARRIERS = {
    "Standard": (
        ["USPS", "UPS", "FedEx"],
        [45, 35, 20],
    ),
    "Two-Day": (
        ["UPS", "FedEx"],
        [50, 50],
    ),
    "Next-Day": (
        ["UPS", "FedEx"],
        [40, 60],
    ),
}

DELIVERY_OUTCOME_WEIGHTS ={
    "Delivered": 99,
    "Lost": 0.5,
    "Damaged": 0.5,
}

DELAY_PROBABILITY = 0.03

#=PAYMENTS====================================================

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Apple Pay",
    "Google Pay"
]

PAYMENT_METHOD_WEIGHTS = [
    60,
    20,
    15,
    10,
    5
]

FIRST_ATTEMPT_SUCCESS_RATE = 0.92
RETRY_PROBABILITY = 0.75
RETRY_SUCCESS_RATE = 0.85


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def round_currency(value):
    return value.quantize(
        CURRENCY_PRECISION,
        rounding=ROUND_HALF_UP
    )

def random_date(start: date, end: date) -> date:
    """Return a random date between start and end, inclusive."""
    number_of_days = (end - start).days
    return start + timedelta(days=random.randint(0, number_of_days))


def calculate_orders_for_year(
    join_date: date,
    shopping_profile: str,
    year: int,
    start_date: date,
    end_date: date,
) -> int:
    """
    Calculate how many orders a customer should place during one year.
    
    Customers who join partway through a year receive a prorated number
    of orders based on how much of that year they were active.
    """

    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    
    #Do not generate activity outside the project's date range.
    year_start = max(year_start, start_date)
    year_end = min(year_end, end_date)
    
    #The customer had not joined yet or this year falls outside
    #the project's date range.
    if join_date > year_end or year_start > end_date:
        return 0
    
    active_start_date = max(join_date, year_start)
    
    active_days = (year_end - active_start_date).days + 1
    total_days_in_year = (year_end - year_start).days + 1
    
    active_year_fraction = active_days / total_days_in_year
    
    minimum_orders, maximum_orders = (
        SHOPPING_PROFILE_ORDER_RANGES[shopping_profile]
    )

    full_year_order_target = random.randint(
        minimum_orders, 
        maximum_orders,
    )


    prorated_order_count = round(
        full_year_order_target * active_year_fraction
    )

    # A customer active during the year should have a at least one order.
    return max(1, prorated_order_count)


def determine_shipping(loyalty_tier, subtotal):
    shipping_method = random.choices(
        SHIPPING_METHODS,
        weights = SHIPPING_METHOD_WEIGHTS,
        k=1
    )[0]
    
    qualifies_for_free_shipping = (
        loyalty_tier == "Platinum"
        or subtotal >= FREE_SHIPPING_THRESHOLD
    )
    
    if qualifies_for_free_shipping:
        shipping_charge = Decimal("0.00")
    else:
        shipping_charge = SHIPPING_RATES[shipping_method]
        
    return shipping_method, shipping_charge



def build_order_items_lookup(order_items):
    """Group all order items by OrderID."""
    order_items_lookup = {}
    
    for item in order_items:
        order_id = item["OrderID"]
        
        if order_id not in order_items_lookup:
            order_items_lookup[order_id] = []
            
        order_items_lookup[order_id].append(item)
        
    return order_items_lookup


def build_product_lookup(products):
    """Group Products by ProductID."""
    product_lookup = {}
    
    for product in products:
        product_lookup[product["ProductID"]] = product
        
    return product_lookup


def build_successful_payments_lookup(payments):
    """Group all successful payments by OrderID."""
    successful_payments_lookup = {}
    
    for payment in payments:
        if payment["PaymentStatus"] == "Successful":
            order_id = payment["OrderID"]
            successful_payments_lookup[order_id] = payment
            
    return successful_payments_lookup


def generate_tracking_number(carrier):
    """Generate a realistic tracking number for the selected carrier."""
    
    if carrier == "USPS":
        return (
            f"9400 " 
            f"{random.randint(1000, 9999)} "
            f"{random.randint(1000, 9999)} "
            f"{random.randint(1000, 9999)}"
        )
            
    elif carrier == ("UPS"):
        return ( 
            f"1Z"
            f"{random.randint(
                1000000000000000, 
                9999999999999999)}"
        )
        
    elif carrier == ("FedEx"):
        tracking_number = str(
            random.randint(
                100000000000000,
                999999999999999,
            )
        )

        return (
            f"{tracking_number[:5]} "
            f"{tracking_number[5:10]} "
            f"{tracking_number[10:]}"
        )
    
    else:
        raise ValueError(f"Unknown carrier: {carrier}")

# ============================================================
# DATA GENERATION FUNCTIONS
# ============================================================

def generate_customers(
    number_of_customers,
    start_date,
    end_date,
) -> list[dict]:
    """Create customer records with realistic demographic distributions."""
    customers = []

    region_names = list(REGION_WEIGHTS.keys())
    region_weights = list(REGION_WEIGHTS.values())

    segment_names = list(CUSTOMER_SEGMENT_WEIGHTS.keys())
    segment_weights = list(CUSTOMER_SEGMENT_WEIGHTS.values())

    loyalty_tiers = list(LOYALTY_TIER_WEIGHTS.keys())
    loyalty_weights = list(LOYALTY_TIER_WEIGHTS.values())

    shopping_profiles = list(SHOPPING_PROFILE_WEIGHTS.keys())
    shopping_profile_weights = list(SHOPPING_PROFILE_WEIGHTS.values())
    
    
    
    
    for customer_id in range(1, number_of_customers + 1):
        gender = random.choices(
            ["Female", "Male", "Nonbinary", "Prefer not to say"],
            weights=[49, 48, 2, 1],
            k=1,
        )[0]

        if gender == "Male":
            first_name = random.choice(MALE_FIRST_NAMES)
        elif gender == "Female":
            first_name = random.choice(FEMALE_FIRST_NAMES)
        else:
            first_name = random.choice(
                MALE_FIRST_NAMES + FEMALE_FIRST_NAMES
            )

        last_name = random.choice(LAST_NAMES)

        region = random.choices(
            region_names,
            weights=region_weights,
            k=1,
        )[0]

        city, state = random.choice(LOCATION_PROFILES[region])

        customer_segment = random.choices(
            segment_names,
            weights=segment_weights,
            k=1,
        )[0]

        loyalty_tier = random.choices(
            loyalty_tiers,
            weights=loyalty_weights,
            k=1,
        )[0]

        join_date = random_date(start_date, end_date)

        birth_year = random.randint(1945, 2005)

        shopping_profile = random.choices(
            shopping_profiles,
            weights=shopping_profile_weights,
            k=1,
        )[0]

        # CustomerID guarantees that every generated email is unique.
        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{customer_id}@"
            f"{random.choice(EMAIL_DOMAINS)}"
        )

        phone = (
            f"({random.randint(200, 999)}) "
            f"{random.randint(200, 999)}-"
            f"{random.randint(1000, 9999)}"
        )

        # Most customers remain active, while older accounts have
        # a slightly greater chance of becoming inactive.
        account_age_days = (end_date - join_date).days
        inactive_probability = min(
            0.05 + (account_age_days / 10_000),
            0.18,
        )

        is_active = random.choices(
            ["Yes", "No"],
            weights=[
                1 - inactive_probability,
                inactive_probability,
            ],
            k=1,
        )[0]

        customers.append(
            {
                "CustomerID": customer_id,
                "FirstName": first_name,
                "LastName": last_name,
                "Email": email,
                "Phone": phone,
                "City": city,
                "State": state,
                "Region": region,
                "BirthYear": birth_year,
                "Gender": gender,
                "JoinDate": join_date.isoformat(),
                "CustomerSegment": customer_segment,
                "LoyaltyTier": loyalty_tier,
                "ShoppingProfile": shopping_profile,
                "IsActive": is_active,
            }
        )

    return customers

def generate_categories() -> list[dict]:
    """Create one record for each product category."""
    categories = []

    for category_id, category_name in enumerate(CATEGORY_PROFILES, start=1):
        categories.append(
            {
                "CategoryID": category_id,
                "CategoryName": category_name,
            }
        )

    return categories


def generate_products(
    categories: list[dict],
    end_date: date,
) -> list[dict]:
    """Create 15 products per category for a total of 120 products."""
    products = []
    product_id = 1

    category_lookup = {
        category["CategoryName"]: category["CategoryID"]
        for category in categories
    }

    launch_date_start = date(2021, 1, 1)

    for category_name, profile in CATEGORY_PROFILES.items():
        category_id = category_lookup[category_name]
        minimum_price, maximum_price = profile["price_range"]

        for adjective in profile["adjectives"]:
            for noun in profile["nouns"]:
                unit_price = round_currency(
                    Decimal(str(random.uniform(minimum_price, maximum_price)))
                )

                # Product cost is generally 45%–70% of its selling price.
                cost_rate = Decimal(
                    str(random.uniform(0.45, 0.70))
                )

                unit_cost = round_currency(
                    unit_price * cost_rate
                )

                products.append(
                    {
                        "ProductID": product_id,
                        "CategoryID": category_id,
                        "ProductName": f"Northstar {adjective} {noun}",
                        "UnitPrice": unit_price,
                        "UnitCost": unit_cost,
                        "LaunchDate": random_date(
                            launch_date_start,
                            end_date,
                        ).isoformat(),
                        "IsActive": random.choices(
                            ["Yes", "No"],
                            weights=[95, 5],
                            k=1,
                        )[0],
                    }
                )

                product_id += 1

    if len(products) != NUMBER_OF_PRODUCTS:
        raise ValueError(
            f"Expected {NUMBER_OF_PRODUCTS} products, "
            f"but generated {len(products)}."
        )

    return products



def generate_orders(
    customers: list[dict],
    start_date: date,
    end_date: date,
) -> list[dict]:
    """Create realistic customer order histories."""
    orders = []
    
    next_order_id = 1

    for customer in customers:
        customer_id = customer["CustomerID"]
        join_date = date.fromisoformat(customer["JoinDate"])
        shopping_profile = customer["ShoppingProfile"]

        for year in range(start_date.year, end_date.year + 1):
            number_of_orders = calculate_orders_for_year(
                join_date=join_date,
                shopping_profile=shopping_profile,
                year=year,
                start_date=start_date,
                end_date=end_date,
            )
                
            if number_of_orders == 0:
                continue

            year_start = date(year, 1, 1)
            year_end = date(year, 12, 31)

            order_start_date = max(year_start, join_date, start_date)
            order_end_date = min(year_end, end_date)

            order_dates = []
            days_in_range = (order_end_date - order_start_date).days

            for _ in range(number_of_orders):
                random_day_offset = random.randint(0, days_in_range)
                order_date = order_start_date + timedelta(days=random_day_offset)
                order_dates.append(order_date)
            
            order_dates.sort()

            for order_date in order_dates:
                order_hour = random.choices(
                    ORDER_HOURS,
                    weights = ORDER_HOUR_WEIGHTS,
                    k=1
                )[0]
                
                order_minute = random.randint(0, 59)
                order_second = random.randint(0, 59)
                
                order_datetime = datetime.combine(
                    order_date,
                    datetime.min.time(),
                ).replace(
                    hour=order_hour,
                    minute=order_minute,
                    second=order_second,
                )
                                
                
                order = {
                    "OrderID": next_order_id,
                    "CustomerID": customer_id,
                    "OrderDateTime": order_datetime.isoformat(sep=" "),
                }

                orders.append(order)
                next_order_id += 1
            
            
    return orders



def generate_order_items(orders, products):
    """
    Generate order items for each order
    """
    
    order_items = []
    next_order_item_id = 1
    
    # Shopping cart settings
    cart_sizes = [1, 2, 3, 4, 5]
    weights = [45, 30, 15, 7, 3]
    
    for order in orders:
        order_datetime = datetime.fromisoformat(order["OrderDateTime"])
        order_date = order_datetime.date()
        
        available_products = [
            product for product in products
            if date.fromisoformat(product["LaunchDate"]) <= order_date
        ]
        
        cart_size = random.choices(
            cart_sizes,
            weights=weights,
            k=1
        )[0]
        
        if not available_products:
            raise ValueError(
                f"No products were available for order "
                f"{order['OrderID']} on {order['OrderDateTime']}"
            )
        
        actual_cart_size = min(
            cart_size,
            len(available_products)
        )

        selected_products = random.sample(
            available_products,
            k=actual_cart_size
        )

        for product in selected_products:
            if product["UnitPrice"] < 20:
                profile = PRICE_TIER_PROFILES["low"]

            elif product["UnitPrice"] < 100:
                profile = PRICE_TIER_PROFILES["medium"]

            elif product["UnitPrice"] < 500:
                profile = PRICE_TIER_PROFILES["high"]

            else:
                profile = PRICE_TIER_PROFILES["premium"]

            quantity = random.choices(
                profile["quantities"],
                weights=profile["weights"],
                k=1
            )[0]

            line_total = round(quantity * product["UnitPrice"], 2,)

            order_item = {
                "OrderItemID": next_order_item_id,
                "OrderID": order["OrderID"],
                "ProductID": product["ProductID"],
                "Quantity": quantity,
                "UnitPrice": product["UnitPrice"],
                "LineTotal": line_total
            }

            order_items.append(order_item)
            next_order_item_id += 1

    return order_items


def finalize_orders(orders, order_items_lookup, customer_lookup):

    for order in orders:
        subtotal = Decimal("0.00")
        customer = customer_lookup[order["CustomerID"]]
        loyalty_tier = customer["LoyaltyTier"]
        
        items = order_items_lookup[order["OrderID"]]

        for item in items:
            subtotal += item["LineTotal"]

        # Determine spend-based discount
        if subtotal < Decimal("100.00"):
            spend_discount_rate = Decimal("0.00")
        elif subtotal < Decimal("250.00"):
            spend_discount_rate = Decimal("0.05")
        elif subtotal < Decimal("500.00"):
            spend_discount_rate = Decimal("0.10")
        else:
            spend_discount_rate = Decimal("0.15")

        # Determine promotional discount
        promotion_discount_rate = random.choices(
            [
                Decimal("0.00"),
                Decimal("0.10"),
                Decimal("0.20"),
            ],
            weights=[80, 15, 5],
            k=1
        )[0]

        # Apply whichever discount is greater
        discount_rate = max(
            spend_discount_rate,
            promotion_discount_rate
        )

        discount_amount = round_currency(
            subtotal * discount_rate
        )
        
        discounted_subtotal = subtotal - discount_amount
        
        shipping_method, shipping = determine_shipping(
            loyalty_tier,
            discounted_subtotal
        )
        
        tax = round_currency(
            (discounted_subtotal + shipping) * Decimal("0.07")
        )

        total = round_currency(
            discounted_subtotal + shipping + tax
        )

        order["Subtotal"] = round_currency(subtotal)
        order["DiscountRate"] = discount_rate
        order["DiscountAmount"] = discount_amount
        order["ShippingMethod"] = shipping_method
        order["Shipping"] = round_currency(shipping)
        order["Tax"] = tax
        order["Total"] = total

    return orders


def generate_payments(orders):

    payments = []
    next_payment_id = 1

    for order in orders:

        payment_method = random.choices(
            PAYMENT_METHODS,
            weights=PAYMENT_METHOD_WEIGHTS,
            k=1,
        )[0]

        first_attempt_succeeds = (
            random.random() < FIRST_ATTEMPT_SUCCESS_RATE
        )

        if first_attempt_succeeds:
            payment_status = "Successful"
        else:
            payment_status = "Failed"

        order_datetime = datetime.fromisoformat(
            order["OrderDateTime"]
        )

        payment_datetime = order_datetime + timedelta(
            seconds=random.randint(5, 120)
        )

        payment = {
            "PaymentID": next_payment_id,
            "OrderID": order["OrderID"],
            "PaymentAttempt": 1,
            "PaymentDateTime": payment_datetime.isoformat(sep=" "),
            "PaymentMethod": payment_method,
            "PaymentAmount": order["Total"],
            "PaymentStatus": payment_status,
        }

        payments.append(payment)
        next_payment_id += 1

        if payment_status == "Failed":
            customer_retries = (
                random.random() < RETRY_PROBABILITY
            )

            if customer_retries:

                retry_succeeds = (
                    random.random() < RETRY_SUCCESS_RATE
                )

                if retry_succeeds:
                    retry_payment_status = "Successful"
                else:
                    retry_payment_status = "Failed"

                retry_delay = timedelta(
                    minutes=random.randint(1, 1440)
                )

                retry_payment_datetime = (
                    payment_datetime + retry_delay
                )

                keeps_same_method = random.random() < 0.80

                if keeps_same_method:
                    retry_payment_method = payment_method
                else:
                    alternative_methods = [
                        method
                        for method in PAYMENT_METHODS
                        if method != payment_method
                    ]

                    retry_payment_method = random.choice(
                        alternative_methods
                    )

                retry_payment = {
                    "PaymentID": next_payment_id,
                    "OrderID": order["OrderID"],
                    "PaymentAttempt": 2,
                    "PaymentDateTime": (
                        retry_payment_datetime.isoformat(sep=" ")
                    ),
                    "PaymentMethod": retry_payment_method,
                    "PaymentAmount": order["Total"],
                    "PaymentStatus": retry_payment_status,
                }

                payments.append(retry_payment)
                next_payment_id += 1

    return payments
    
    
#ShipmentDateTime represents teh actual shipment time for completed
#shipments and the scheduled shipmnet time for orders tstill proscessing.
def generate_shipments(orders, payments):
    """Generate shipment records for orders with successful payments."""

    successful_payments_lookup = (
        build_successful_payments_lookup(payments)
    )

    shipments = []
    next_shipment_id = 1

    for order in orders:
        order_id = order["OrderID"]

        if order_id not in successful_payments_lookup:
            continue

        successful_payment = successful_payments_lookup[order_id]

        payment_datetime = datetime.fromisoformat(
            successful_payment["PaymentDateTime"]
        )

        if payment_datetime > CURRENT_DATETIME:
            continue
        
        shipping_method = order["ShippingMethod"]
        
        carriers, carrier_weights = SHIPPING_CARRIERS[shipping_method]
        
        carrier = random.choices(
            carriers,
            weights=carrier_weights,
            k=1
        )[0]

        minimum_hours, maximum_hours = (
            SHIPPING_PROCESSING_HOURS[shipping_method]
        )

        ship_datetime = payment_datetime + timedelta(
            hours=random.randint(
                minimum_hours,
                maximum_hours,
            )
        )


        minimum_days, maximum_days = (
            SHIPPING_TRANSIT_DAYS[shipping_method]
        )
        
        estimated_delivery_datetime = (
            ship_datetime 
            + timedelta(
                days=random.randint(
                    minimum_days,
                    maximum_days,
                )
            )
        )

        
        tracking_number = generate_tracking_number(carrier)
        
        actual_delivery_datetime = None
        is_delayed = False
                
        if CURRENT_DATETIME < ship_datetime:
            shipment_status = "Processing"

        elif CURRENT_DATETIME < estimated_delivery_datetime:
            shipment_status = "In Transit"

        else:
            shipment_status = random.choices(
                list(DELIVERY_OUTCOME_WEIGHTS.keys()),
                weights=list(DELIVERY_OUTCOME_WEIGHTS.values()),
                k=1,
            )[0]

            if shipment_status == "Delivered":
                is_delayed = random.random() < DELAY_PROBABILITY

                if is_delayed:
                    planned_delivery_datetime = (
                        estimated_delivery_datetime
                        + timedelta(days=random.randint(1, 5))
                    )

                    if planned_delivery_datetime <= CURRENT_DATETIME:
                        actual_delivery_datetime = planned_delivery_datetime
                    else:
                        shipment_status = "In Transit"
                        actual_delivery_datetime = None

                else:
                    actual_delivery_datetime = (
                        estimated_delivery_datetime
                        - timedelta(days=random.randint(0, 1))
                    )
                    
            
        shipment = {
            "ShipmentID": next_shipment_id,
            "OrderID": order_id,
            "Carrier": carrier,
            "TrackingNumber": tracking_number,
            "ShipmentDateTime": ship_datetime.isoformat(sep=" "),
            "EstimatedDeliveryDateTime": estimated_delivery_datetime.isoformat(
                sep=" "
            ),
            "ActualDeliveryDateTime": (
                actual_delivery_datetime.isoformat(sep=" ")
                if actual_delivery_datetime is not None
                else ""
            ),
            "ShipmentStatus": shipment_status,
            "IsDelayed": is_delayed,
            "ShippingMethod": shipping_method,
            "ShippingCost": order["Shipping"],
        }



        shipments.append(shipment)
        next_shipment_id += 1

    return shipments   
# ============================================================
# CSV EXPORT FUNCTIONS
# ============================================================

def write_csv(
    file_path: Path,
    records: list[dict],
    fieldnames: list[str],
) -> None:
    """Write a list of dictionaries to a CSV file."""
    with file_path.open(
        mode="w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(records)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main() -> None:
    print("Northstar Commerce data generator")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Raw data folder: {RAW_DATA_FOLDER}")
    print()

    print("Generator configuration:")
    print(f"Customers: {NUMBER_OF_CUSTOMERS:,}")
    print(f"Products: {NUMBER_OF_PRODUCTS:,}")
    #print(f"Orders: {TARGET_NUMBER_OF_ORDERS:,}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print()

    customers = generate_customers(
        NUMBER_OF_CUSTOMERS,
        START_DATE,
        END_DATE
    )
    
    customer_lookup = {
        customer["CustomerID"]: customer 
        for customer in customers
    }
    
    categories = generate_categories()
    products = generate_products(
        categories,
        END_DATE
    )
    product_lookup = build_product_lookup(products)
    orders = generate_orders(
        customers,
        START_DATE,
        END_DATE,
    )
    order_items = generate_order_items(orders, products)
    order_items_lookup = build_order_items_lookup(order_items)
    

    orders = finalize_orders(
        orders,
        order_items_lookup,
        customer_lookup
    )

    payments = generate_payments(orders)
    shipments = generate_shipments(orders, payments)

    write_csv(
    CUSTOMERS_FILE,
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
        CATEGORIES_FILE,
        categories,
        ["CategoryID", "CategoryName"],
    )

    write_csv(
        PRODUCTS_FILE,
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
        ORDERS_FILE,
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
        ]
    )

    write_csv(
        ORDER_ITEMS_FILE,
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
        PAYMENTS_FILE,
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
    
    
    write_csv(
        SHIPMENTS_FILE,
        shipments,
        [
            "ShipmentID",
            "OrderID",
            "Carrier",
            "TrackingNumber",
            "ShipmentDateTime",
            "EstimatedDeliveryDateTime",
            "ActualDeliveryDateTime",
            "ShipmentStatus",
            "IsDelayed",
            "ShippingMethod",
            "ShippingCost",
        ],
    )

    print("Files created successfully:")
    print(f"- {CUSTOMERS_FILE.name}: {len(customers):,} rows")
    print(f"- {CATEGORIES_FILE.name}: {len(categories):,} rows")
    print(f"- {PRODUCTS_FILE.name}: {len(products):,} rows")
    print(f"- {ORDERS_FILE.name}: {len(orders):,} rows")
    print(f"- {ORDER_ITEMS_FILE.name}: {len(order_items):,} rows")
    print(f"- {PAYMENTS_FILE.name}: {len(payments):,} rows")
    print(f"- {SHIPMENTS_FILE.name}: {len(shipments):,} rows")


if __name__ == "__main__":
    main()