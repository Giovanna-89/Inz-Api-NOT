from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.password_change_due():
            if request.path != reverse('users:password_change'):
                return redirect('users:password_change')
        return self.get_response(request)