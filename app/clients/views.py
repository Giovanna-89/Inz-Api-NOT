from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from core.models import Kontrahent, Powiat, Zadanie, Wojewodztwo
from .forms import KontrahentCreateForm, KontrahentUpdateForm, PowiatCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class KontrahentListView(LoginRequiredMixin, ListView):
    model = Kontrahent
    template_name = 'clients/kontrahent_list.html'
    context_object_name = 'kontrahenci'
    success_url = reverse_lazy('clients:kontrahenci')

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        sort = self.request.GET.get('sort', 'nazwa_kontrahenta')
        direction = self.request.GET.get('direction', 'asc')

        if search:
            queryset = queryset.filter(
                Q(nazwa_kontrahenta__icontains=search) |
                Q(typ_kontrahenta__nazwa__icontains=search) |
                Q(powiat__nazwa__icontains=search) |
                Q(powiat__wojewodztwo__nazwa__icontains=search)
            )

        valid_sort_options = ['nazwa_kontrahenta', 'typ_kontrahenta__nazwa', 'powiat__wojewodztwo__nazwa', 'powiat__nazwa']
        if sort in valid_sort_options:
            if direction == 'desc':
                sort = f'-{sort}'
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'nazwa_kontrahenta')
        context['direction'] = self.request.GET.get('direction', 'asc')
        context['search'] = self.request.GET.get('search', '')
        context['wojewodztwa'] = Wojewodztwo.objects.all()
        context['powiaty'] = Powiat.objects.all().select_related('wojewodztwo')
        return context

class KontrahentCreateView(LoginRequiredMixin, CreateView):
    model = Kontrahent
    form_class = KontrahentCreateForm
    template_name = 'clients/kontrahent_create.html'
    success_url = reverse_lazy('clients:kontrahenci')

    def get_initial(self):
        initial = super().get_initial()
        powiat_id = self.request.GET.get('powiat')
        if powiat_id:
            initial['powiat'] = powiat_id
        return initial
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wojewodztwa'] = Wojewodztwo.objects.all()
        context['powiaty'] = Powiat.objects.all()  
        return contextS

class KontrahentUpdateView(LoginRequiredMixin, UpdateView):
    model = Kontrahent
    form_class = KontrahentUpdateForm
    template_name = 'clients/kontrahent_update.html'
    success_url = reverse_lazy('clients:kontrahenci')

class KontrahentDetailView(LoginRequiredMixin, DetailView):
    model = Kontrahent
    template_name = 'clients/kontrahent_detail.html'
    context_object_name = 'kontrahent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zadania'] = Zadanie.objects.filter(kontrahent=self.object).order_by('nazwa_zadania')
        return context

class PowiatCreateView(LoginRequiredMixin, CreateView):
    model = Powiat
    form_class = PowiatCreateForm
    template_name = 'clients/powiat_create.html'

    def form_valid(self, form):
        wojewodztwo = form.cleaned_data['wojewodztwo']
        nazwa = form.cleaned_data['nazwa']
        
        # Sprawdź, czy powiat o tej nazwie w danym województwie już istnieje
        if Powiat.objects.filter(nazwa=nazwa, wojewodztwo=wojewodztwo).exists():
            form.add_error(None, "Powiat o tej nazwie w tym województwie już istnieje.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        next_url = self.request.GET.get('next', None)
        if next_url:
            return redirect(next_url)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wojewodztwa'] = Wojewodztwo.objects.all()  # Przekazuje listę województw do szablonu
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('clients:kontrahent_nowy')
