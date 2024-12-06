from django.db import models, connection
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
import json

# Violation 1: Function-based user management
def create_user(request):
    data = json.loads(request.body)
    
    # Violation 2: Direct user creation without repository
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # Violation 3: Direct group assignment
    if 'group' in data:
        group = Group.objects.get(name=data['group'])
        user.groups.add(group)
    
    return JsonResponse({'id': user.id})

# Violation 4: Mixed authentication and user management
def update_user_status(user_id, status):
    # Violation 5: Direct model update
    User.objects.filter(id=user_id).update(is_active=status)
    
    # Violation 6: Raw SQL for audit log
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_audit_log 
            (user_id, action, timestamp) 
            VALUES (%s, %s, NOW())
        """, [user_id, f"Status changed to {status}"])

# Violation 7: Bulk operations without repository
def bulk_user_update(user_ids, data):
    # Violation 8: Direct bulk update
    User.objects.filter(id__in=user_ids).update(**data)

# Violation 9: Complex queries outside repository
def get_user_permissions(user_id):
    # Violation 10: Complex ORM query
    user = User.objects.prefetch_related(
        'groups__permissions',
        'user_permissions'
    ).get(id=user_id)
    
    # Violation 11: Business logic mixed with data access
    permissions = set()
    for group in user.groups.all():
        permissions.update(group.permissions.values_list('codename', flat=True))
    permissions.update(user.user_permissions.values_list('codename', flat=True))
    
    return list(permissions)

# Violation 12: Direct model access in utility function
def cleanup_inactive_users():
    # Violation 13: Hard delete without repository
    User.objects.filter(
        is_active=False,
        last_login__isnull=True
    ).delete()

# Violation 14: Authentication mixed with email logic
def send_user_welcome_email(user_id):
    # Violation 15: Direct user query
    user = User.objects.get(id=user_id)
    
    # Violation 16: Business logic mixed with data access
    from django.core.mail import send_mail
    send_mail(
        'Welcome',
        f'Welcome {user.username}!',
        'from@example.com',
        [user.email]
    )