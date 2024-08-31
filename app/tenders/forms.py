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
            'wartosc_zadania', 'wycena'
        ]

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        wycena = cleaned_data.get("wycena")

        if status and status.nazwa in ['W trakcie', 'Zakończony'] and wycena == 0:
            self.add_error('wycena', "Wycena nie może być równa 0 dla statusu 'W trakcie' lub 'Zakończony'.")

        return cleaned_data

class ZadanieUpdateForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = ['status', 'termin_statusu', 'wycena']
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
    class Meta:
        model = SpecjalistaZadania
        fields = ['specjalista', 'wycena_wykonawcy']
    
    def __init__(self, *args, **kwargs):
        # We need to pass the zadanie instance to the form to use it in validation
        self.zadanie = kwargs.pop('zadanie', None)
        super().__init__(*args, **kwargs)

    def clean_specjalista(self):
        specjalista = self.cleaned_data['specjalista']

        # Check if the specialist is already assigned to this task
        if SpecjalistaZadania.objects.filter(zadanie=self.zadanie, specjalista=specjalista).exists():
            raise forms.ValidationError("Ten specjalista jest już przypisany do tego zadania.")
        
        return specjalista

class RodzajZadaniaCreateForm(forms.ModelForm):
    class Meta:
        model = RodzajZadania
        fields = ['nazwa']
