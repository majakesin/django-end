# Generated by Django 3.1.6 on 2021-02-22 11:00

from django.db import migrations, models
import movie.models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=movie.models.upload_path),
        ),
    ]
