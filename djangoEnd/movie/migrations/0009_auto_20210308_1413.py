# Generated by Django 3.1.7 on 2021-03-08 14:13

from django.db import migrations, models
import movie.models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_auto_20210308_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=movie.models.upload_path),
        ),
    ]
