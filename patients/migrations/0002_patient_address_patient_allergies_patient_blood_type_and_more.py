# Generated by Django 5.0.2 on 2025-06-15 21:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="address",
            field=models.TextField(blank=True, verbose_name="Adres"),
        ),
        migrations.AddField(
            model_name="patient",
            name="allergies",
            field=models.TextField(
                blank=True,
                help_text="Bilinen alerjileri yazın",
                verbose_name="Alerjiler",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="blood_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("A+", "A Rh+"),
                    ("A-", "A Rh-"),
                    ("B+", "B Rh+"),
                    ("B-", "B Rh-"),
                    ("AB+", "AB Rh+"),
                    ("AB-", "AB Rh-"),
                    ("O+", "O Rh+"),
                    ("O-", "O Rh-"),
                    ("", "Bilinmiyor"),
                ],
                max_length=3,
                verbose_name="Kan Grubu",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="city",
            field=models.CharField(blank=True, max_length=100, verbose_name="İl"),
        ),
        migrations.AddField(
            model_name="patient",
            name="district",
            field=models.CharField(blank=True, max_length=100, verbose_name="İlçe"),
        ),
    ]
