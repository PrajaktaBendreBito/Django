from django.db import models, connection
from datetime import datetime

# Violation 1: Mixed approach (partial class usage)
class OrderHandler:
    def __init__(self):
        # Violation 2: Direct ORM in constructor
        self.pending_orders = Order.objects.filter(status='pending')

    # Violation 3: Direct model access
    def process_order(self, order_id):
        order = Order.objects.get(id=order_id)
        order.status = 'processing'
        order.save()

# Violation 4: Function-based approach with direct ORM
def get_order_stats():
    # Violation: Complex query outside repository
    return Order.objects.values('status').annotate(
        count=models.Count('id'),
        total_amount=models.Sum('amount')
    )

# Violation 5: Raw SQL with business logic
def update_bulk_orders(status):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE orders_order 
            SET status = %s, 
                updated_at = %s 
            WHERE status = 'pending'
        """, [status, datetime.now()])

# Violation 6: Direct model operations in utility function
def cancel_old_orders():
    Order.objects.filter(
        created_at__lt=datetime.now() - timedelta(days=30),
        status='pending'
    ).update(status='cancelled')

# Violation 7: Multiple responsibilities
def process_refund(order_id):
    order = Order.objects.get(id=order_id)
    # Direct payment processing
    process_payment_refund(order.payment_id)
    # Direct email sending
    send_refund_email(order.user.email)
    # Direct order update
    order.status = 'refunded'
    order.save()