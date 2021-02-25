# Generated by Django 3.1.6 on 2021-02-24 14:34

from django.db import migrations, models
import movie.models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDislikeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('type', models.BooleanField()),
                ('user_id', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=movie.models.upload_path),
        ),
    ]