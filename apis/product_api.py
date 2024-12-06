from django.db import models
from django.db.models import F, Sum, Count
from django.http import JsonResponse

# Violation 1: Mixed class/function approach
class ProductAPI:
    # Violation 2: Direct ORM in constructor
    def __init__(self):
        self.products = Product.objects.all()

    # Violation 3: Direct ORM queries in methods
    def get_product(self, product_id):
        return Product.objects.get(id=product_id)

# Violation 4: Function with direct ORM and complex logic
def get_product_analytics(category_id=None):
    query = Product.objects.all()
    if category_id:
        query = query.filter(category_id=category_id)
    
    # Violation: Complex annotations outside repository
    return query.annotate(
        revenue=F('price') * F('sales_count'),
        profit_margin=(F('price') - F('cost')) / F('price') * 100
    ).values('id', 'name', 'revenue', 'profit_margin')

# Violation 5: Direct model updates with business logic
def update_product_inventory(product_id, quantity):
    product = Product.objects.get(id=product_id)
    if product.stock < quantity:
        raise ValueError("Insufficient stock")
    
    product.stock -= quantity
    product.sales_count += quantity
    product.save()

# Violation 6: Raw SQL for analytics
def get_top_products():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.name, SUM(o.quantity * p.price) as revenue
            FROM products_product p
            JOIN order_items oi ON p.id = oi.product_id
            GROUP BY p.id, p.name
            ORDER BY revenue DESC
            LIMIT 10
        """)
        return cursor.fetchall()

# Violation 7: Multiple concerns in one function
def process_product_return(product_id, order_id):
    # Direct ORM queries
    product = Product.objects.get(id=product_id)
    order = Order.objects.get(id=order_id)
    
    # Direct inventory update
    product.stock += 1
    product.returns_count += 1
    product.save()
    
    # Direct order update
    order.status = 'returned'
    order.save()
    
    # Direct email notification
    send_return_confirmation(order.user.email)