from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from core.models import Zadanie, SpecjalistaZadania, RodzajZadania, Specjalista
from .forms import ZadanieCreateForm, ZadanieUpdateForm, SpecjalistaZadaniaForm
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
        sort = self.request.GET.get('sort', 'termin_statusu')
        direction = self.request.GET.get('direction', 'asc')

        if search:
            queryset = queryset.filter(
                Q(nazwa_zadania__icontains=search) |
                Q(kontrahent__nazwa_kontrahenta__icontains=search) |
                Q(kontrahent__typ_kontrahenta__nazwa__icontains=search) |  # Dodano pole `nazwa`
                Q(rodzaj_zadania__nazwa__icontains=search) |
                Q(status__nazwa__icontains=search) |
                Q(przypisany_pracownik__first_name__icontains=search) |
                Q(przypisany_pracownik__last_name__icontains=search)
            )

        valid_sort_options = [
        'nazwa_zadania', 'termin_statusu', 'kontrahent__nazwa_kontrahenta',
        'kontrahent__typ_kontrahenta__nazwa', 'rodzaj_zadania__nazwa',
        'status__nazwa', 'przypisany_pracownik__first_name',
        'przypisany_pracownik__last_name'
        ]
        if sort in valid_sort_options:
            if direction == 'desc':
                sort = f'-{sort}'
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'termin_statusu')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

class ZadanieCreateView(LoginRequiredMixin, CreateView):
    model = Zadanie
    form_class = ZadanieCreateForm
    template_name = 'tenders/zadanie_create.html'
    success_url = reverse_lazy('tenders:przetargi')

    def form_valid(self, form):
        form.instance.przypisany_pracownik = self.request.user
        if form.instance.status.nazwa in ['W trakcie', 'Zakończony']:
            if form.instance.wycena == 0:
                form.add_error('wycena', "Wycena nie może być równa 0.")
                return self.form_invalid(form)
        return super().form_valid(form)

class ZadanieUpdateView(LoginRequiredMixin, UpdateView):
    model = Zadanie
    form_class = ZadanieUpdateForm
    template_name = 'tenders/zadanie_update.html'
    success_url = reverse_lazy('tenders:przetargi')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zadanie = self.object
        context['zadanie'] = zadanie
        context['kontrahent'] = zadanie.kontrahent
        context['przypisani_specjalisci'] = SpecjalistaZadania.objects.filter(zadanie=zadanie)
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        zadanie = self.object

        # Ustawienia dostępności pól w zależności od statusu zadania
        if zadanie.status.nazwa in ['W trakcie', 'Zakończony']:
            form.fields['wycena'].disabled = True
            form.fields['data_wprowadzenia'].disabled = True
        if zadanie.status.nazwa == 'Zakończony':
            form.fields['status'].disabled = True
            form.fields['termin_statusu'].disabled = True

        return form

    def form_valid(self, form):
        zadanie = form.save()
        if zadanie.status.nazwa == 'Zakończony':
            form.fields['status'].disabled = True
            return super().form_valid(form)

        if zadanie.status.nazwa in ['W trakcie', 'Zakończony']:
            for specjalista in form.cleaned_data['specjalisci']:
                SpecjalistaZadania.objects.get_or_create(
                    zadanie=zadanie,
                    specjalista=specjalista,
                    defaults={'wycena_wykonawcy': 0}
                )

        return super().form_valid(form)

class ZadanieDetailView(LoginRequiredMixin, DetailView):
    model = Zadanie
    template_name = 'tenders/zadanie_detail.html'
    context_object_name = 'zadanie'

class SpecjalistaZadanieView(LoginRequiredMixin, CreateView):
    model = SpecjalistaZadania
    form_class = SpecjalistaZadaniaForm
    template_name = 'tenders/specjalista_zadania.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zadanie'] = get_object_or_404(Zadanie, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        zadanie = get_object_or_404(Zadanie, pk=self.kwargs['pk'])
        specjalista = form.cleaned_data['specjalista']

        # Sprawdzenie, czy specjalista jest już przypisany do zadania
        if SpecjalistaZadania.objects.filter(zadanie=zadanie, specjalista=specjalista).exists():
            messages.error(self.request, "Ten specjalista jest już przypisany do tego zadania.")
            return self.form_invalid(form)

        form.instance.zadanie = zadanie
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tenders:zadanie_szczegoly', kwargs={'pk': self.kwargs['pk']})

