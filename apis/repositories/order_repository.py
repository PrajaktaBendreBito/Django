from django.db import models
from typing import List, Dict, Any
from datetime import datetime, timedelta

class OrderRepository:
    @classmethod
    def get_pending_orders(cls):
        return Order.objects.filter(status='pending')
    
    @classmethod
    def update_order_status(cls, order_id: int, status: str) -> None:
        Order.objects.filter(id=order_id).update(
            status=status,
            updated_at=datetime.now()
        )
    
    @classmethod
    def get_order_stats(cls) -> Dict[str, Any]:
        return Order.objects.values('status').annotate(
            count=models.Count('id'),
            total_amount=models.Sum('amount')
        )
    
    @classmethod
    def update_bulk_orders(cls, old_status: str, new_status: str) -> int:
        return Order.objects.filter(status=old_status).update(
            status=new_status,
            updated_at=datetime.now()
        )
    
    @classmethod
    def cancel_old_orders(cls, days: int = 30) -> int:
        return Order.objects.filter(
            created_at__lt=datetime.now() - timedelta(days=days),
            status='pending'
        ).update(status='cancelled')