from django.views import View
from django.http import JsonResponse
from .repositories.order_repository import OrderRepository
from .services.payment_service import PaymentService
from .services.notification_service import NotificationService

class OrderProcessView(View):
    def post(self, request, order_id):
        OrderRepository.update_order_status(order_id, 'processing')
        return JsonResponse({'status': 'success'})

class OrderStatsView(View):
    def get(self, request):
        stats = OrderRepository.get_order_stats()
        return JsonResponse({'stats': list(stats)})

class OrderRefundView(View):
    def post(self, request, order_id):
        # Using service layer for business logic
        PaymentService.process_refund(order_id)
        OrderRepository.update_order_status(order_id, 'refunded')
        NotificationService.send_refund_notification(order_id)
        return JsonResponse({'status': 'success'})