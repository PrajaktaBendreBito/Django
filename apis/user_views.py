from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# Bug 1: Using function-based views instead of class-based views
@require_http_methods(["GET"])
def get_user_details(request, user_id):
    # Bug 2: Direct ORM query outside repository
    user = User.objects.filter(id=user_id).first()
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

# Bug 3: Another function-based view with direct queries
@require_http_methods(["GET"])
def search_users(request):
    query = request.GET.get('q', '')
    # Bug 4: Complex ORM query outside repository
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query)
    ).values('id', 'username', 'email')
    return JsonResponse({'users': list(users)})

# Bug 5: Raw SQL query in view
@require_http_methods(["GET"])
def get_active_users(request):
    from django.db import connection
    with connection.cursor() as cursor:
        # Bug 6: Direct SQL query outside repository
        cursor.execute("""
            SELECT id, username, email 
            FROM auth_user 
            WHERE is_active = true
        """)
        rows = cursor.fetchall()
    return JsonResponse({'users': rows})