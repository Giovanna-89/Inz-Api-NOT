from django.urls import path
from .views import SpecjalistaListView, SpecjalistaCreateView, SpecjalistaUpdateView, SpecjalistaDetailView

urlpatterns = [
    path('specjalisci/', SpecjalistaListView.as_view(), name='specjalisci'),
    path('specjalista/nowy/', SpecjalistaCreateView.as_view(), name='specjalista_nowy'),
    path('specjalista/<int:pk>/edytuj/', SpecjalistaUpdateView.as_view(), name='specjalista_edytuj'),
    path('specjalista/<int:pk>/', SpecjalistaDetailView.as_view(), name='specjalista_szczegoly'),
]
