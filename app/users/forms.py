from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from core.models import User
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'position')
        labels = {
            'email': _('E-mail'),
            'first_name': _('Imię'),
            'last_name': _('Nazwisko'),
            'position': _('Stanowisko'),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'position')
        labels = {
            'email': _('E-mail'),
            'first_name': _('Imię'),
            'last_name': _('Nazwisko'),
            'position': _('Stanowisko'),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': _('E-mail'),
            'password': _('Hasło'),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ("Nowe hasło musi zawierać co najmniej 12 znaków, w tym co najmniej", 
                                                "\n- jedną cyfrę",
                                                "\n- jedną małą literę", 
                                                "\n- jedną dużą literę",
                                                "\n- jeden znak specjalny",)
    
    old_password = forms.CharField(
        label=_("Stare hasło"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password1 = forms.CharField(
        label=_("Nowe hasło"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Potwierdź nowe hasło"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

class Meta:
    fields = ('old_password', 'new_password1', 'new_password2')

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 12:
            raise forms.ValidationError(_("Hasło musi mieć co najmniej 12 znaków."))
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(_("Hasło musi zawierać co najmniej jedną cyfrę."))
        if not any(char.islower() for char in password):
            raise forms.ValidationError(_("Hasło musi zawierać co najmniej jedną małą literę."))
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(_("Hasło musi zawierać co najmniej jedną dużą literę."))
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
            raise forms.ValidationError(_("Hasło musi zawierać co najmniej jeden znak specjalny."))
        return password