from django import forms
from core.models import Zadanie, SpecjalistaZadania, Specjalista, RodzajZadania

class ZadanieCreateForm(forms.ModelForm):
    data_wprowadzenia = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    termin_statusu = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    specjalisci = forms.ModelMultipleChoiceField(
        queryset=Specjalista.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Zadanie
        fields = [
            'nazwa_zadania', 'kontrahent', 'rodzaj_zadania', 'status', 'data_wprowadzenia', 'termin_statusu',
            'wartosc_zadania', 'wycena', 'specjalisci'
        ]

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        wycena = cleaned_data.get("wycena")

        if status and status.nazwa in ['W trakcie', 'Zakończony'] and wycena == 0:
            self.add_error('wycena', "Wycena nie może być równa 0 dla statusu 'W trakcie' lub 'Zakończony'.")

        return cleaned_data

class ZadanieUpdateForm(forms.ModelForm):
    specjalisci = forms.ModelMultipleChoiceField(
        queryset=Specjalista.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False
    )

    class Meta:
        model = Zadanie
        fields = ['status', 'termin_statusu', 'wycena', 'specjalisci']
        widgets = {
            'data_wprowadzenia': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'termin_statusu': forms.DateInput(attrs={'type': 'date'}),
            'wycena': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }    

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        wycena = cleaned_data.get("wycena")

        if status and status.nazwa in ['W trakcie', 'Zakończony'] and wycena == 0:
            self.add_error('wycena', "Wycena nie może być równa 0 dla statusu 'W trakcie' lub 'Zakończony'.")

        return cleaned_data


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
