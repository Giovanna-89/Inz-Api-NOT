from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('przetargi/', include('tenders.urls', namespace='tenders')),
    path('', RedirectView.as_view(url='/users/login/', permanent=True)),
    path('clients/', include('clients.urls')),
    path('specialists/', include('specialists.urls')),
    path('reports/', include('reports.urls')),
]
