from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from core.models import Zadanie, SpecjalistaZadania
from .forms import ZadanieCreateForm, ZadanieUpdateForm, SpecjalistaZadaniaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

class PrzetargiListView(LoginRequiredMixin, ListView):
    model = Zadanie
    template_name = 'tenders/przetargi_list.html'
    context_object_name = 'zadania'

class ZadanieCreateView(LoginRequiredMixin, CreateView):
    model = Zadanie
    form_class = ZadanieCreateForm
    template_name = 'tenders/zadanie_form.html'
    success_url = reverse_lazy('tenders:przetargi')

    def form_valid(self, form):
        form.instance.przypisany_pracownik = self.request.user
        return super().form_valid(form)

class ZadanieUpdateView(LoginRequiredMixin, UpdateView):
    model = Zadanie
    form_class = ZadanieUpdateForm
    template_name = 'tenders/zadanie_form.html'
    success_url = reverse_lazy('tenders:przetargi')

class ZadanieDetailView(LoginRequiredMixin, DetailView):
    model = Zadanie
    template_name = 'tenders/zadanie_detail.html'
    context_object_name = 'zadanie'

class ZadanieAssignView(LoginRequiredMixin, FormView):
    form_class = SpecjalistaZadaniaForm
    template_name = 'tenders/zadanie_assign_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zadanie'] = get_object_or_404(Zadanie, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        zadanie = get_object_or_404(Zadanie, pk=self.kwargs['pk'])
        specjalista_zadania, created = SpecjalistaZadania.objects.get_or_create(
            zadanie=zadanie,
            specjalista=form.cleaned_data['specjalista']
        )
        specjalista_zadania.wycena_wykonawcy = form.cleaned_data['wycena_wykonawcy']
        specjalista_zadania.save()
        return redirect('tenders:zadanie_szczegoly', pk=zadanie.pk)
