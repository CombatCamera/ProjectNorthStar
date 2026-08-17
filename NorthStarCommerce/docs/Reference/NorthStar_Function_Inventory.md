# Helper Functions
def random_date(start: date, end: date) -> date:
def calculate_orders_for_year(join_date: date, shopping_profile: str, year:int,) -> int:
def determine_shipping(loyalty_tier, subtotal): 
def build_order_items_lookup(order_items):
def build_product_lookup(products):
def build_successful_payments_lookup(payments):
def generate_tracking_number(carrier):


# Customer Generation
def generate_customers() -> list[dict]:


# Product Generation
def generate_categories() -> list[dict]:
def generate_products(categories: list[dict]) -> list[dict]:


# Order Generation
def generate_orders(customers: list[dict]) -> list[dict]:
def generate_order_items(orders, products):
def finalize_orders(orders, order_items_lookup, customer_lookup):


# Payment Generation
def generate_payments(orders):


# Shipping Generation
def generate_shipments(orders, payments):


# QA Validation
separate module


# CSV
def write_csv(file_path: Path, records: list[dict], fieldnames: list[str],) -> None:


# Main
def main() -> None:

