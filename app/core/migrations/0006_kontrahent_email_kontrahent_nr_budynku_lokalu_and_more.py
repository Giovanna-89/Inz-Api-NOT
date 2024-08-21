# Generated by Django 4.2.15 on 2024-08-17 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_specjalista_rodzaj_uprawnien_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="kontrahent",
            name="email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="kontrahent",
            name="nr_budynku_lokalu",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="kontrahent",
            name="telefon",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]