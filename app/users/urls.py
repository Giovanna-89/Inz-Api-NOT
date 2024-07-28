from django.urls import path
from .views import CustomLoginView, CustomPasswordChangeView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
