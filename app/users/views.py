from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect

User = get_user_model()

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.password_change_due():
            return redirect('password_change')
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change.html'

    def form_valid(self, form):
        form.save()
        self.request.user.password_change_date = timezone.now()
        self.request.user.save()
        return super().form_valid(form)
