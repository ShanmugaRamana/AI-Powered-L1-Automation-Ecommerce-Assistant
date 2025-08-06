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
def process_return_request(order_number: str, reason: str) -> dict:
    """Simulates processing a return request."""
    print(f"TOOL USED: Processing return for order #{order_number} due to: {reason}")
    if order_number in ["101", "102", "103"]:
        return {
            "status": "success",
            "message": f"I've started the return process for order #{order_number}. You will receive an email with instructions shortly."
        }
    else:
        return {
            "status": "error",
            "message": "I couldn't find that order number to process a return."
        }
def request_human_agent(issue: str) -> dict:
    """
    Simulates escalating the conversation to a human agent by creating a support ticket.
    """
    ticket_id = f"TICKET-{random.randint(1000, 9999)}"
    print("="*30)
    print("!! HUMAN ESCALATION TRIGGERED !!")
    print(f"  Ticket ID: {ticket_id}")
    print(f"  User Issue: {issue}")
    print("="*30)
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": f"A support ticket ({ticket_id}) has been created. An agent will review the issue and contact the user shortly."
    }