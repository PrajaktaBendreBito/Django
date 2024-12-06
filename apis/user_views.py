from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Q, Count

# Violation 1: Function-based view instead of class-based
def get_users(request):
    # Violation 2: Direct ORM query in view
    users = User.objects.all()
    return JsonResponse({'users': list(users.values())})

# Violation 3: Raw SQL in view
def get_active_users(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM auth_user 
            WHERE is_active = True
        """)
        rows = cursor.fetchall()
    return JsonResponse({'active_users': rows})

# Violation 4: Complex queries outside repository
def search_users(request):
    query = request.GET.get('q', '')
    # Violation: Complex ORM query in view
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query)
    ).annotate(
        login_count=Count('login_logs')
    )
    return JsonResponse({'results': list(users.values())})

# Violation 5: Direct model manipulation
def update_user_status(request, user_id):
    # Violation: Direct model update
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'status': 'success'})