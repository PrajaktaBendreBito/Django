from django.db import models
from django.http import JsonResponse
from datetime import datetime

# Bug 1: Mixed approach - partial class usage but mostly functions
class OrderStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

# Bug 2: Direct model access outside repository
def get_order_by_id(order_id):
    from orders.models import Order
    return Order.objects.get(id=order_id)

# Bug 3: Function with direct ORM operations
def process_order(request, order_id):
    from orders.models import Order, OrderItem
    
    # Bug 4: Multiple direct ORM queries
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order_id=order_id)
    
    # Bug 5: Direct update without repository
    order.status = OrderStatus.COMPLETED
    order.processed_at = datetime.now()
    order.save()
    
    return JsonResponse({
        'order_id': order.id,
        'status': order.status,
        'items': list(items.values())
    })

# Bug 6: Direct bulk operations without repository
def bulk_cancel_orders(order_ids):
    from orders.models import Order
    Order.objects.filter(id__in=order_ids).update(
        status=OrderStatus.CANCELLED,
        cancelled_at=datetime.now()
    )

# Bug 7: Raw SQL for complex queries
def get_order_statistics():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM orders_order
            GROUP BY status
        """)
        return dict(cursor.fetchall())