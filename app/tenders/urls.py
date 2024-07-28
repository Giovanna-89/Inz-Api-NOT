from django.urls import path
from .views import PrzetargiListView, ZadanieCreateView, ZadanieUpdateView, ZadanieDetailView, ZadanieAssignView

app_name = 'tenders'

urlpatterns = [
    path('', PrzetargiListView.as_view(), name='przetargi'),
    path('zadanie/nowe/', ZadanieCreateView.as_view(), name='zadanie_nowe'),
    path('zadanie/<int:pk>/edytuj/', ZadanieUpdateView.as_view(), name='zadanie_edytuj'),
    path('zadanie/<int:pk>/', ZadanieDetailView.as_view(), name='zadanie_szczegoly'),
    path('zadanie/<int:pk>/przypisz/', ZadanieAssignView.as_view(), name='zadanie_przypisz'),
]
