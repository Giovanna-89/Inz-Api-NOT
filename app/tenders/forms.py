from django import forms
from core.models import Zadanie

class ZadanieCreateForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = [
            'nazwa_zadania', 'kontrahent', 'rodzaj_zadania', 'status', 'termin_statusu', 
            'wartosc_zadania', 'wycena', 'wykonawca', 'wycena_wykonawcy'
        ]

class ZadanieUpdateForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = ['status', 'termin_statusu', 'wycena', 'wykonawca', 'wycena_wykonawcy']
