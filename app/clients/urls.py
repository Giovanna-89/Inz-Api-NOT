from django.urls import path
from .views import KontrahentListView, KontrahentCreateView, KontrahentUpdateView, KontrahentDetailView, PowiatCreateView

app_name = 'clients'

urlpatterns = [
    path('', KontrahentListView.as_view(), name='kontrahenci'),
    path('nowy/', KontrahentCreateView.as_view(), name='kontrahent_nowy'),
    path('<int:pk>/edytuj/', KontrahentUpdateView.as_view(), name='kontrahent_edytuj'),
    path('<int:pk>/', KontrahentDetailView.as_view(), name='kontrahent_szczegoly'),
    path('dodaj-powiat/', PowiatCreateView.as_view(), name='powiat_nowy'),
]
