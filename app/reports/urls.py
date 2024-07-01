from django.urls import path
from .views import RaportView

urlpatterns = [
    path('raport/', RaportView.as_view(), name='raport'),
]
