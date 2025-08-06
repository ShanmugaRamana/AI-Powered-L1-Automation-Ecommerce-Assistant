# /backend/app/services/ecommerce_service.py
import random
from datetime import datetime, timedelta

# --- MOCK E-COMMERCE API ---
# In a real application, this would make an HTTP request to your store's backend.
def check_order_status(order_number: str) -> dict:
    """
    Simulates checking an order status.
    Returns a dictionary with order information or an error.
    """
    print(f"TOOL USED: Checking status for order #{order_number}")
    
    # Simulate some real order numbers
    if order_number in ["101", "102", "103"]:
        delivery_date = (datetime.now() + timedelta(days=random.randint(1, 4))).strftime("%A, %B %d")
        statuses = ["Shipped", "Out for Delivery", "In Transit"]
        return {
            "status": "success",
            "order_number": order_number,
            "shipping_status": random.choice(statuses),
            "estimated_delivery": delivery_date
        }
    else:
        # Simulate an order that doesn't exist
        return {
            "status": "error",
            "message": f"Sorry, I couldn't find any order with the number {order_number}."
        }