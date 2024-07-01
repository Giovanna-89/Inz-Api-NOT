from django import forms
from core.models import Specjalista

class SpecjalistaCreateForm(forms.ModelForm):
    class Meta:
        model = Specjalista
        fields = ['imie', 'nazwisko', 'branza', 'rodzaj_uprawnien', 'telefon', 'email', 'obszar_dzialania']

class SpecjalistaUpdateForm(forms.ModelForm):
    class Meta:
        model = Specjalista
        fields = ['branza', 'rodzaj_uprawnien', 'telefon', 'email', 'obszar_dzialania']

