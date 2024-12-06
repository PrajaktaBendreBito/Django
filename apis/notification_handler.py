from django.db import connection
from django.contrib.auth.models import User
from django.core.mail import send_mail
import json

# Violation 1: Function-based instead of class-based
def send_notification(user_id, message):
    # Violation 2: Direct ORM query outside repository
    user = User.objects.get(id=user_id)
    
    # Violation 3: Raw SQL query in business logic
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT email FROM auth_user 
            WHERE id = %s AND is_active = True
        """, [user_id])
        email = cursor.fetchone()[0]
    
    # Violation 4: Business logic mixed with data access
    send_mail(
        'Notification',
        message,
        'from@example.com',
        [email],
        fail_silently=False,
    )

# Violation 5: Multiple responsibilities in single function
def process_bulk_notifications():
    # Violation 6: Complex ORM query outside repository
    users = User.objects.filter(is_active=True).exclude(email='').values('id', 'email')
    
    # Violation 7: Direct database updates
    User.objects.filter(id__in=[u['id'] for u in users]).update(notification_sent=True)
    
    return users

# Violation 8: Authentication mixed with notification logic
def notify_authenticated_users(message):
    # Violation 9: Hardcoded values
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.email, u.first_name 
            FROM auth_user u 
            JOIN auth_user_groups g ON u.id = g.user_id 
            WHERE g.group_id = 1
        """)
        users = cursor.fetchall()
    
    for user in users:
        send_mail('Auth Notification', message, 'from@example.com', [user[0]])