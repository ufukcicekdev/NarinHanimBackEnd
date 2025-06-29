# Generated by Django 5.0.2 on 2025-06-16 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0005_patient_patient_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="VisitStage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "stage_number",
                    models.PositiveIntegerField(verbose_name="Etap Numarası"),
                ),
                ("date", models.DateTimeField(verbose_name="Etap Tarihi")),
                (
                    "complaint",
                    models.TextField(
                        help_text="Hastanın bu etaptaki şikayetleri",
                        verbose_name="Şikayet",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Etap Notları")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "visit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stages",
                        to="patients.visit",
                    ),
                ),
            ],
            options={
                "ordering": ["stage_number"],
                "unique_together": {("visit", "stage_number")},
            },
        ),
        migrations.CreateModel(
            name="StageMedicine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="İlaç Adı")),
                ("dosage", models.CharField(max_length=100, verbose_name="Doz")),
                (
                    "frequency",
                    models.CharField(max_length=100, verbose_name="Kullanım Sıklığı"),
                ),
                (
                    "duration",
                    models.CharField(max_length=100, verbose_name="Kullanım Süresi"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="İlaç Notları")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medicines",
                        to="patients.visitstage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StageEyeImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "eye_type",
                    models.CharField(
                        choices=[("left", "Sol Göz"), ("right", "Sağ Göz")],
                        max_length=5,
                        verbose_name="Göz",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="stage_eye_images/", verbose_name="Göz Fotoğrafı"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Açıklama")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eye_images",
                        to="patients.visitstage",
                    ),
                ),
            ],
        ),
    ]
