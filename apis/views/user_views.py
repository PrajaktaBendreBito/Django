from django.views import View
from django.http import JsonResponse
from .repositories.user_repository import UserRepository

class UserView(View):
    def get(self, request):
        users = UserRepository.get_all_users()
        return JsonResponse({'users': users})

class ActiveUserView(View):
    def get(self, request):
        active_users = UserRepository.get_active_users()
        return JsonResponse({'active_users': active_users})

class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        results = UserRepository.search_users(query)
        return JsonResponse({'results': results})

class UserStatusView(View):
    def post(self, request, user_id):
        status = request.POST.get('status', False)
        UserRepository.update_user_status(user_id, status)
        return JsonResponse({'status': 'success'})