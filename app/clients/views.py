from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from core.models import Kontrahent
from .forms import KontrahentCreateForm, KontrahentUpdateForm

class KontrahentListView(ListView):
    model = Kontrahent
    template_name = 'clients/kontrahent_list.html'
    context_object_name = 'kontrahenci'

class KontrahentCreateView(CreateView):
    model = Kontrahent
    form_class = KontrahentCreateForm
    template_name = 'clients/kontrahent_form.html'
    success_url = reverse_lazy('kontrahenci')

class KontrahentUpdateView(UpdateView):
    model = Kontrahent
    form_class = KontrahentUpdateForm
    template_name = 'clients/kontrahent_form.html'
    success_url = reverse_lazy('kontrahenci')

class KontrahentDetailView(DetailView):
    model = Kontrahent
    template_name = 'clients/kontrahent_detail.html'
    context_object_name = 'kontrahent'
