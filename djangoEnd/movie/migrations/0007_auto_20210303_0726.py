# Generated by Django 3.1.7 on 2021-03-03 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_auto_20210225_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image_url_omdb',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(max_length=600),
        ),
    ]
