from django.urls import path
from .views import (
    SpecjalistaListView, 
    SpecjalistaCreateView, 
    SpecjalistaUpdateView, 
    SpecjalistaDetailView, 
    SpecjalistaObszarDzialaniaView, 
    SpecjalistaBranzaUprawnieniaView
)

app_name = 'specialists'

urlpatterns = [
    path('specjalisci/', SpecjalistaListView.as_view(), name='specjalisci'),
    path('specjalista/nowy/', SpecjalistaCreateView.as_view(), name='specjalista_nowy'),
    path('specjalista/<int:pk>/edytuj/', SpecjalistaUpdateView.as_view(), name='specjalista_edytuj'),
    path('specjalista/<int:pk>/', SpecjalistaDetailView.as_view(), name='specjalista_szczegoly'),
    path('specjalista/<int:pk>/obszar_dzialania/', SpecjalistaObszarDzialaniaView.as_view(), name='specjalista_obszar_dzialania'),
    path('specjalista/<int:pk>/branza_uprawnienia/', SpecjalistaBranzaUprawnieniaView.as_view(), name='specjalista_branza_uprawnienia'),
]
