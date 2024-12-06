from django.db import models, connection
from typing import List, Dict, Any
from datetime import datetime

class UserRepository:
    @classmethod
    def get_all_users(cls) -> List[Dict[str, Any]]:
        return list(User.objects.all().values())
    
    @classmethod
    def get_active_users(cls) -> List[Dict[str, Any]]:
        return list(User.objects.filter(is_active=True).values())
    
    @classmethod
    def search_users(cls, query: str) -> List[Dict[str, Any]]:
        return list(User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).annotate(
            login_count=Count('login_logs')
        ).values())
    
    @classmethod
    def update_user_status(cls, user_id: int, status: bool) -> None:
        User.objects.filter(id=user_id).update(is_active=status)