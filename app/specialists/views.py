from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from core.models import Specjalista
from .forms import SpecjalistaCreateForm, SpecjalistaUpdateForm

class SpecjalistaListView(ListView):
    model = Specjalista
    template_name = 'specialists/specjalista_list.html'
    context_object_name = 'specjalisci'

class SpecjalistaCreateView(CreateView):
    model = Specjalista
    form_class = SpecjalistaCreateForm
    template_name = 'specialists/specjalista_form.html'
    success_url = reverse_lazy('specjalisci')

class SpecjalistaUpdateView(UpdateView):
    model = Specjalista
    form_class = SpecjalistaUpdateForm
    template_name = 'specialists/specjalista_form.html'
    success_url = reverse_lazy('specjalisci')

class SpecjalistaDetailView(DetailView):
    model = Specjalista
    template_name = 'specialists/specjalista_detail.html'
    context_object_name = 'specjalista'
