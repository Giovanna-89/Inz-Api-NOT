from django import forms
from core.models import Zadanie, SpecjalistaZadania, Specjalista, RodzajZadania

class ZadanieCreateForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = [
            'nazwa_zadania', 'kontrahent', 'rodzaj_zadania', 'status', 'data_wprowadzenia', 'termin_statusu', 
            'wartosc_zadania', 'wycena'
        ]

class ZadanieUpdateForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = ['status', 'termin_statusu', 'wycena']

class SpecjalistaZadaniaForm(forms.ModelForm):
    specjalista = forms.ModelChoiceField(queryset=Specjalista.objects.all(), widget=forms.Select)
    wycena_wykonawcy = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = SpecjalistaZadania
        fields = ['specjalista', 'wycena_wykonawcy']

class RodzajZadaniaCreateForm(forms.ModelForm):
    class Meta:
        model = RodzajZadania
        fields = ['nazwa']