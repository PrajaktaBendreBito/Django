from django.db import models, connection
from django.db.models import Sum, Count
from django.http import JsonResponse

# Violation 1: Direct model imports and usage
from django.contrib.auth.models import User
from myapp.models import Order, Product

# Violation 2: Function-based analytics instead of class-based
def get_sales_analytics(start_date, end_date):
    # Violation 3: Complex ORM query outside repository
    sales_data = Order.objects.filter(
        created_at__range=[start_date, end_date]
    ).annotate(
        total_amount=Sum('items__price'),
        item_count=Count('items')
    ).values('user_id', 'total_amount', 'item_count')
    
    # Violation 4: Direct user queries
    user_ids = [sale['user_id'] for sale in sales_data]
    users = User.objects.filter(id__in=user_ids).values('id', 'email')
    
    return {'sales': list(sales_data), 'users': list(users)}

# Violation 5: Raw SQL analytics
def product_performance():
    # Violation 6: Complex SQL outside repository
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.name,
                COUNT(oi.id) as total_orders,
                SUM(oi.quantity) as total_quantity,
                AVG(oi.price) as avg_price
            FROM product_product p
            LEFT JOIN orderitem_orderitem oi ON p.id = oi.product_id
            GROUP BY p.id, p.name
            ORDER BY total_orders DESC
        """)
        return cursor.fetchall()

# Violation 7: Mixed business logic and data access
def update_product_analytics():
    # Violation 8: Direct model updates
    products = Product.objects.all()
    for product in products:
        sales_count = Order.objects.filter(
            items__product=product
        ).count()
        
        product.total_sales = sales_count
        product.save()

# Violation 9: Authentication mixed with analytics
def get_user_analytics(user_id):
    # Violation 10: Multiple direct queries
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)
    
    # Violation 11: Complex calculations outside service layer
    total_spent = sum(order.total_amount for order in orders)
    order_count = orders.count()
    
    return {
        'user_email': user.email,
        'total_spent': total_spent,
        'order_count': order_count
    }

# Violation 12: Bulk operations without repository
def bulk_analytics_update():
    # Violation 13: Direct bulk updates
    Product.objects.all().update(analytics_updated=True)
    
    # Violation 14: Raw SQL for analytics
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE analytics_productmetrics
            SET views_count = subquery.views
            FROM (
                SELECT product_id, COUNT(*) as views
                FROM product_views
                GROUP BY product_id
            ) AS subquery
            WHERE analytics_productmetrics.product_id = subquery.product_id
        """)