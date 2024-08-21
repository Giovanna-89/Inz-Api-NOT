from django import forms
from core.models import Specjalista, Branza, Powiat, SpecjalistaBranza, RodzajUprawnien, ObszarDzialania

class SpecjalistaObszarDzialaniaForm(forms.ModelForm):
    class Meta:
        model = ObszarDzialania
        fields = ['powiat']

class SpecjalistaBranzaUprawnieniaForm(forms.ModelForm):
    branza = forms.ModelChoiceField(queryset=Branza.objects.all(), label="Branża")
    rodzaj_uprawnien = forms.ModelChoiceField(queryset=RodzajUprawnien.objects.all(), label="Uprawnienia")

    class Meta:
        model = SpecjalistaBranza
        fields = ['branza', 'rodzaj_uprawnien']

class SpecjalistaBranzaForm(forms.ModelForm):
    branza = forms.ModelChoiceField(queryset=Branza.objects.all(), required=True, label="Branża")
    rodzaj_uprawnien = forms.ModelChoiceField(queryset=RodzajUprawnien.objects.all(), required=True, label="Rodzaj uprawnień")

    class Meta:
        model = SpecjalistaBranza
        fields = ['branza', 'rodzaj_uprawnien']

class SpecjalistaCreateForm(forms.ModelForm):
    branzo_uprawnienia = forms.ModelMultipleChoiceField(
        queryset=Branza.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Branże z uprawnieniami"
    )
    obszar_dzialania = forms.ModelMultipleChoiceField(
        queryset=Powiat.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label="Obszar działania (Powiaty)"
    )

    class Meta:
        model = Specjalista
        fields = ['imie', 'nazwisko', 'telefon', 'email', 'obszar_dzialania']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            # Zapis branż i uprawnień
            SpecjalistaBranza.objects.filter(specjalista=instance).delete()
            for branza in self.cleaned_data['branzo_uprawnienia']:
                rodzaj_uprawnien = self.data.get(f'rodzaj_uprawnien_{branza.id}')
                SpecjalistaBranza.objects.create(specjalista=instance, branza=branza, rodzaj_uprawnien_id=rodzaj_uprawnien)
        return instance

class SpecjalistaUpdateForm(SpecjalistaCreateForm):
    class Meta(SpecjalistaCreateForm.Meta):
        pass
