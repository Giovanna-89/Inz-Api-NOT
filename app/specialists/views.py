from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from core.models import Specjalista, SpecjalistaBranza, ObszarDzialania, Powiat, Branza, RodzajUprawnien, Zadanie, Wojewodztwo
from .forms import SpecjalistaCreateForm, SpecjalistaUpdateForm, SpecjalistaObszarDzialaniaForm, SpecjalistaBranzaUprawnieniaForm
from django.contrib import messages
from django.db.models import Q

class SpecjalistaListView(ListView):
    model = Specjalista
    template_name = 'specialists/specjalista_list.html'
    context_object_name = 'specjalisci'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'specjalistabranza_set__branza',
            'specjalistabranza_set__rodzaj_uprawnien',
            'obszardzialania_set__powiat',
            'obszardzialania_set__powiat__wojewodztwo'
        )
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(imie__icontains=search_query) | 
                Q(nazwisko__icontains=search_query)
            )
        return queryset.order_by(self.get_ordering())

    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'nazwisko')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            ordering = f'-{ordering}'
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'nazwisko')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

class SpecjalistaCreateView(CreateView):
    model = Specjalista
    form_class = SpecjalistaCreateForm
    template_name = 'specialists/specjalista_create.html'
    success_url = reverse_lazy('specialists:specjalisci')

    def form_valid(self, form):
        if Specjalista.objects.filter(imie=form.cleaned_data['imie'], 
                                      nazwisko=form.cleaned_data['nazwisko'],
                                      email=form.cleaned_data['email']).exists():
            messages.error(self.request, "Specjalista o takim imieniu, nazwisku i emailu już istnieje.")
            return self.form_invalid(form)
        return super().form_valid(form)

class SpecjalistaUpdateView(UpdateView):
    model = Specjalista
    form_class = SpecjalistaUpdateForm
    template_name = 'specialists/specjalista_update.html'
    success_url = reverse_lazy('specialists:specjalisci')

    def form_valid(self, form):
        if not form.cleaned_data['telefon'] and not form.cleaned_data['email']:
            messages.error(self.request, "Proszę podać numer telefonu lub adres email.")
            return self.form_invalid(form)
        return super().form_valid(form)

class SpecjalistaDetailView(DetailView):
    model = Specjalista
    template_name = 'specialists/specjalista_detail.html'
    context_object_name = 'specjalista'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branze'] = SpecjalistaBranza.objects.filter(specjalista=self.object)
        context['obszary_dzialania'] = ObszarDzialania.objects.filter(specjalista=self.object)
        context['zadania'] = Zadanie.objects.filter(specjalistazadania__specjalista=self.object)
        return context

class SpecjalistaObszarDzialaniaView(CreateView):
    model = ObszarDzialania
    form_class = SpecjalistaObszarDzialaniaForm
    template_name = 'specialists/obszar_dzialania.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wojewodztwa'] = Wojewodztwo.objects.all()
        context['powiaty'] = Powiat.objects.all()
        return context

    def form_valid(self, form):
        specjalista = get_object_or_404(Specjalista, pk=self.kwargs['pk'])
        powiat = form.cleaned_data['powiat']
        if ObszarDzialania.objects.filter(specjalista=specjalista, powiat=powiat).exists():
            messages.error(self.request, "Ten obszar działania już został dodany.")
            return self.form_invalid(form)
        form.instance.specjalista = specjalista
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('specialists:specjalista_szczegoly', kwargs={'pk': self.kwargs['pk']})

class SpecjalistaBranzaUprawnieniaView(UpdateView):
    model = Specjalista
    template_name = 'specialists/branza_uprawnienia.html'
    fields = []  # Formularz jest niestandardowy, więc pola są obsługiwane w szablonie
    success_url = reverse_lazy('specialists:specjalisci')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_branze'] = Branza.objects.all()
        context['available_uprawnienia'] = RodzajUprawnien.objects.all()
        context['branze'] = SpecjalistaBranza.objects.filter(specjalista=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        branza_id = request.POST.get('branza')
        uprawnienia_id = request.POST.get('rodzaj_uprawnien')
        if branza_id and uprawnienia_id:
            if SpecjalistaBranza.objects.filter(specjalista=self.object, branza_id=branza_id, rodzaj_uprawnien_id=uprawnienia_id).exists():
                messages.error(request, "Ta branża z tymi uprawnieniami już została dodana.")
            else:
                SpecjalistaBranza.objects.create(specjalista=self.object, branza_id=branza_id, rodzaj_uprawnien_id=uprawnienia_id)
                messages.success(request, "Branża i uprawnienia zostały dodane.")
        return redirect(self.get_success_url())