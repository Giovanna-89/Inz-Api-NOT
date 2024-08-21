from django import forms
from core.models import Kontrahent, Powiat, Wojewodztwo
import re

class PowiatCreateForm(forms.ModelForm):
    class Meta:
        model = Powiat
        fields = ['nazwa', 'wojewodztwo']

class KontrahentCreateForm(forms.ModelForm):
    wojewodztwo = forms.ModelChoiceField(queryset=Wojewodztwo.objects.all(), label="Województwo", required=True)

    class Meta:
        model = Kontrahent
        fields = ['nazwa_kontrahenta', 'typ_kontrahenta', 'ulica', 'nr_budynku_lokalu', 'kod_pocztowy', 'miasto', 'wojewodztwo', 'powiat', 'email', 'telefon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Zamiast początkowo wyłączać pole powiatu, załaduj wszystkie powiaty
        self.fields['powiat'].queryset = Powiat.objects.all().order_by('nazwa')

        if 'wojewodztwo' in self.data:
            try:
                wojewodztwo_id = int(self.data.get('wojewodztwo'))
                self.fields['powiat'].queryset = Powiat.objects.filter(wojewodztwo_id=wojewodztwo_id).order_by('nazwa')
            except (ValueError, TypeError):
                pass  # Invalid input; fallback to all powiaty
        elif self.instance.pk and self.instance.wojewodztwo:
            # Jeśli edytujemy obiekt, ustawiamy powiaty na podstawie wybranego województwa
            self.fields['powiat'].queryset = self.instance.wojewodztwo.powiat_set.order_by('nazwa')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        telefon = cleaned_data.get("telefon")
        kod_pocztowy = cleaned_data.get("kod_pocztowy")

        # Walidacja kontaktu
        if not email and not telefon:
            self.add_error('email', "Musisz podać email lub numer telefonu.")
            self.add_error('telefon', "Musisz podać email lub numer telefonu.")

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.add_error('email', "Nieprawidłowy format adresu email.")

        if kod_pocztowy and not re.match(r"\d{2}-\d{3}", kod_pocztowy):
            self.add_error('kod_pocztowy', "Nieprawidłowy format kodu pocztowego. Użyj formatu XX-XXX.")

        if telefon and not re.match(r"^\d{3}-\d{3}-\d{3}$", telefon):
            self.add_error('telefon', "Nieprawidłowy format numeru telefonu. Użyj formatu XXX-XXX-XXX.")

        return cleaned_data


class KontrahentUpdateForm(forms.ModelForm):
    telefon = forms.CharField(
        max_length=11, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': '000-000-000'})
    )
    email = forms.EmailField(
        required=False, 
        widget=forms.EmailInput(attrs={'placeholder': 'example@domain.com'})
    )

    class Meta:
        model = Kontrahent
        fields = ['telefon', 'email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        telefon = cleaned_data.get("telefon")

        if not email and not telefon:
            self.add_error('email', "Musisz podać email lub numer telefonu.")
            self.add_error('telefon', "Musisz podać email lub numer telefonu.")

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.add_error('email', "Nieprawidłowy format adresu email.")

        if telefon and not re.match(r"^\d{3}-\d{3}-\d{3}$", telefon):
            self.add_error('telefon', "Nieprawidłowy format numeru telefonu. Użyj formatu XXX-XXX-XXX.")

        return cleaned_data
