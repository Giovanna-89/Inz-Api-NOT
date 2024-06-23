from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.password_change_due():
            return redirect('password_change')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('przetargi')

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('przetargi')
    template_name = 'users/password_change.html'

    def form_valid(self, form):
        form.save()
        self.request.user.password_change_date = timezone.now()
        self.request.user.save()
        messages.success(self.request, 'Twoje hasło zostało pomyślnie zmienione.')
        return super().form_valid(form)
