from django import forms
from core.models import Kontrahent

class KontrahentCreateForm(forms.ModelForm):
    class Meta:
        model = Kontrahent
        fields = ['nazwa_kontrahenta', 'typ_kontrahenta', 'ulica', 'kod_pocztowy', 'miasto', 'powiat']

class KontrahentUpdateForm(forms.ModelForm):
    class Meta:
        model = Kontrahent
        fields = ['typ_kontrahenta', 'ulica', 'kod_pocztowy', 'miasto', 'powiat']
