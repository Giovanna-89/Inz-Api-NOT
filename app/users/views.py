from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
import logging

User = get_user_model()

# Konfiguracja loggera
logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)  
        logger.debug(f"CSRF Token on GET: {csrf_token}")
        response = super().get(request, *args, **kwargs)
        response.set_cookie('csrftoken', csrf_token)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Błędne dane logowania. Spróbuj ponownie.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        user = self.request.user
        if user.password_change_due():
            return reverse_lazy('users:password_change')
        return reverse_lazy('tenders:przetargi')

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('tenders:przetargi')
    template_name = 'users/password_change.html'

    def form_valid(self, form):
        logger.debug("Form is valid")
        # Debugowanie
        # logger.debug(f"Old password: {form.cleaned_data.get('old_password')}")
        # logger.debug(f"New password1: {form.cleaned_data.get('new_password1')}")
        # logger.debug(f"New password2: {form.cleaned_data.get('new_password2')}")

        # Sprawdzenie zgodności haseł
        new_password1 = form.cleaned_data.get('new_password1')
        new_password2 = form.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            messages.error(self.request, "Hasła nie są zgodne.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        self.request.user.password_change_date = timezone.now()
        self.request.user.save()
        return response

    def form_invalid(self, form):
        errors = form.errors.as_text()
        logger.error(f"Form errors: {errors}")
        messages.error(self.request, f"Wystąpił błąd podczas zmiany hasła. {errors}")
        return super().form_invalid(form)
