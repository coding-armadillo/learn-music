# Generated by Django 4.0.4 on 2022-05-01 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_album_song_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='gala_piece',
            field=models.BooleanField(default=False),
        ),
    ]
