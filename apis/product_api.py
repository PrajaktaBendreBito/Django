from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import F, Sum, Avg
from products.models import Product, Category

# Bug 1: Mix of class and function-based approaches
class ProductCategory:
    def __init__(self, category_id):
        # Bug 2: Direct ORM query in constructor
        self.category = Category.objects.get(id=category_id)
        
    def get_products(self):
        # Bug 3: Direct ORM query in method
        return Product.objects.filter(category=self.category)

# Bug 4: Function-based view with direct queries
@require_http_methods(["GET"])
def get_product_list(request):
    category_id = request.GET.get('category')
    # Bug 5: Direct ORM with complex query
    products = Product.objects.filter(
        active=True
    ).annotate(
        revenue=F('price') * F('sales_count')
    ).values('id', 'name', 'price', 'revenue')
    return JsonResponse({'products': list(products)})

# Bug 6: Function mixing business logic and data access
def update_product_inventory(product_id, quantity):
    # Bug 7: Direct ORM update
    product = Product.objects.get(id=product_id)
    product.inventory_count += quantity
    product.save()
    
    # Bug 8: Additional direct queries
    if product.inventory_count < product.minimum_threshold:
        from django.core.mail import send_mail
        send_mail(
            'Low Inventory Alert',
            f'Product {product.name} is low on inventory',
            'from@example.com',
            ['to@example.com'],
        )

# Bug 9: Complex analytics with direct SQL
def get_product_analytics():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.category_id,
                c.name as category_name,
                COUNT(*) as product_count,
                AVG(p.price) as avg_price
            FROM products_product p
            JOIN products_category c ON p.category_id = c.id
            GROUP BY p.category_id, c.name
        """)
        return cursor.fetchall()