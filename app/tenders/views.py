from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from core.models import Zadanie, SpecjalistaZadania, RodzajZadania
from .forms import ZadanieCreateForm, ZadanieUpdateForm, SpecjalistaZadaniaForm, RodzajZadaniaCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

class PrzetargiListView(LoginRequiredMixin, ListView):
    model = Zadanie
    template_name = 'tenders/przetargi_list.html'
    context_object_name = 'zadania'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        sort = self.request.GET.get('sort', 'termin_statusu')  # Ustaw domyślne sortowanie

        # Filtruj według zapytania wyszukiwania
        if search:
            queryset = queryset.filter(
                Q(nazwa_zadania__icontains=search) | 
                Q(kontrahent__nazwa_kontrahenta__icontains=search)
            )

        # Sprawdź, czy wybrana opcja sortowania jest dozwolona
        valid_sort_options = ['nazwa_zadania', 'termin_statusu', 'kontrahent__nazwa_kontrahenta']
        if sort in valid_sort_options:
            queryset = queryset.order_by(sort)

        return queryset

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

class RodzajZadaniaCreateView(CreateView):
    model = RodzajZadania
    form_class = RodzajZadaniaCreateForm
    template_name = 'tenders/rodzaj_zadania_form.html'
    success_url = reverse_lazy('tenders:przetargi')
