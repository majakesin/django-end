# Generated by Django 3.1.7 on 2021-03-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_delete_likedislikeoption'),
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
    ]
