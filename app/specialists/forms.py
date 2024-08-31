from django import forms
from core.models import Specjalista, Branza, Powiat, SpecjalistaBranza, RodzajUprawnien, ObszarDzialania

class SpecjalistaObszarDzialaniaForm(forms.ModelForm):
    powiat = forms.ModelMultipleChoiceField(
        queryset=Powiat.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Wybierz powiaty"
    )
    class Meta:
        model = Specjalista  # Musi być tutaj zdefiniowany model
        fields = ['powiat']


class SpecjalistaBranzaUprawnieniaForm(forms.ModelForm):
    class Meta:
        model = SpecjalistaBranza
        fields = ['branza', 'rodzaj_uprawnien']

class SpecjalistaCreateForm(forms.ModelForm):
    class Meta:
        model = Specjalista
        fields = ['imie', 'nazwisko', 'telefon', 'email']


class SpecjalistaUpdateForm(SpecjalistaCreateForm):
    class Meta(SpecjalistaCreateForm.Meta):
        fields = ['telefon', 'email']  # Ograniczono pola do edycji
