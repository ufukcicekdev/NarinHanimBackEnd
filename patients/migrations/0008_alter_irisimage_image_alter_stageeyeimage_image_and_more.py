# Generated by Django 5.0.2 on 2025-06-17 18:24

import patients.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0007_remove_stageeyeimage_eye_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="irisimage",
            name="image",
            field=models.ImageField(upload_to=patients.models.iris_image_upload_path),
        ),
        migrations.AlterField(
            model_name="stageeyeimage",
            name="image",
            field=models.ImageField(
                upload_to=patients.models.stage_eye_image_upload_path,
                verbose_name="Göz Fotoğrafı",
            ),
        ),
        migrations.AlterField(
            model_name="visit",
            name="document",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=patients.models.visit_document_upload_path,
                verbose_name="Ziyaret Dokümanı",
            ),
        ),
    ]
