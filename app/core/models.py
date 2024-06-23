from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, first_name, last_name, position, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, position=position, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, position, password):
        """Create and return a new superuser."""
        user = self.create_user(email, first_name, last_name, position, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password_change_date = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'position']

    def password_change_due(self):
        if not self.password_change_date:
            return True
        return timezone.now() > self.password_change_date + timedelta(days=30)

class Wojewodztwo(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class Powiat(models.Model):
    nazwa = models.CharField(max_length=255)
    wojewodztwo = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa

class Kontrahent(models.Model):
    nazwa_kontrahenta = models.CharField(max_length=255)
    typ_kontrahenta = models.CharField(max_length=255)
    ulica = models.CharField(max_length=255)
    kod_pocztowy = models.CharField(max_length=10)
    miasto = models.CharField(max_length=255)
    powiat = models.ForeignKey(Powiat, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa_kontrahenta

class Typ(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class Status(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class RodzajZadania(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class Specjalista(models.Model):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    branza = models.ForeignKey('Branza', on_delete=models.CASCADE)
    rodzaj_uprawnien = models.ForeignKey('RodzajUprawnien', on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15)
    email = models.EmailField()
    obszar_dzialania = models.ManyToManyField(Powiat, through='ObszarDzialania')

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Branza(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class RodzajUprawnien(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa

class ObszarDzialania(models.Model):
    specjalista = models.ForeignKey(Specjalista, on_delete=models.CASCADE)
    powiat = models.ForeignKey(Powiat, on_delete=models.CASCADE)

class Zadanie(models.Model):
    nazwa_zadania = models.CharField(max_length=255)
    kontrahent = models.ForeignKey(Kontrahent, on_delete=models.CASCADE)
    rodzaj_zadania = models.ForeignKey(RodzajZadania, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    data_wprowadzenia = models.DateField()
    termin_statusu = models.DateField()
    wartosc_zadania = models.DecimalField(max_digits=10, decimal_places=2)
    wycena = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wykonawca = models.CharField(max_length=255)
    wycena_wykonawcy = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    przypisany_pracownik = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa_zadania

class SpecjalistaZadania(models.Model):
    specjalista = models.ForeignKey(Specjalista, on_delete=models.CASCADE)
    zadanie = models.ForeignKey(Zadanie, on_delete=models.CASCADE)