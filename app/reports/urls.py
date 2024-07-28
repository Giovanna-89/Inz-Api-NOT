from django.urls import path
from .views import RaportView

app_name = 'reports'

urlpatterns = [
    path('raport/', RaportView.as_view(), name='raport'),
]
