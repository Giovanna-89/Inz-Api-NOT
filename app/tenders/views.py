from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from core.models import Zadanie
from .forms import ZadanieCreateForm, ZadanieUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

class PrzetargiListView(LoginRequiredMixin, ListView):
    model = Zadanie
    template_name = 'tenders/przetargi_list.html'
    context_object_name = 'zadania'

class ZadanieCreateView(LoginRequiredMixin, CreateView):
    model = Zadanie
    form_class = ZadanieCreateForm
    template_name = 'tenders/zadanie_form.html'
    success_url = reverse_lazy('przetargi')

    def form_valid(self, form):
        form.instance.przypisany_pracownik = self.request.user
        return super().form_valid(form)

class ZadanieUpdateView(LoginRequiredMixin, UpdateView):
    model = Zadanie
    form_class = ZadanieUpdateForm
    template_name = 'tenders/zadanie_form.html'
    success_url = reverse_lazy('przetargi')

class ZadanieDetailView(LoginRequiredMixin, DetailView):
    model = Zadanie
    template_name = 'tenders/zadanie_detail.html'
    context_object_name = 'zadanie'
