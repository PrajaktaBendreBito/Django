from django.db import models, connection
from django.http import JsonResponse
from datetime import datetime

# Violation 1: Mixed approach (partial class usage)
class PaymentProcessor:
    def __init__(self):
        # Violation 2: Direct ORM query in constructor
        self.pending_payments = models.Payment.objects.filter(status='pending')
    
    # Violation 3: Direct database access in method
    def get_payment_status(self, payment_id):
        return models.Payment.objects.get(id=payment_id).status

# Violation 4: Function-based view instead of class-based
def process_payment(request):
    payment_id = request.POST.get('payment_id')
    
    # Violation 5: Raw SQL for payment processing
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE payments_payment 
            SET status = 'processed', 
                processed_at = %s 
            WHERE id = %s
        """, [datetime.now(), payment_id])
    
    return JsonResponse({'status': 'success'})

# Violation 6: Direct model operations in utility function
def bulk_payment_update(payment_ids, status):
    # Violation 7: Complex query outside repository
    models.Payment.objects.filter(id__in=payment_ids).update(
        status=status,
        updated_at=datetime.now()
    )

# Violation 8: Mixed responsibilities
def payment_statistics():
    # Violation 9: Complex raw SQL outside repository
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                status,
                COUNT(*) as count,
                SUM(amount) as total_amount
            FROM payments_payment
            GROUP BY status
        """)
        return cursor.fetchall()

# Violation 10: Direct model access in helper function
def mark_failed_payments():
    models.Payment.objects.filter(
        status='processing',
        created_at__lt=datetime.now()
    ).update(status='failed')