from django.urls import path
from .views import KontrahentListView, KontrahentCreateView, KontrahentUpdateView, KontrahentDetailView

urlpatterns = [
    path('kontrahenci/', KontrahentListView.as_view(), name='kontrahenci'),
    path('kontrahent/nowy/', KontrahentCreateView.as_view(), name='kontrahent_nowy'),
    path('kontrahent/<int:pk>/edytuj/', KontrahentUpdateView.as_view(), name='kontrahent_edytuj'),
    path('kontrahent/<int:pk>/', KontrahentDetailView.as_view(), name='kontrahent_szczegoly'),
]
