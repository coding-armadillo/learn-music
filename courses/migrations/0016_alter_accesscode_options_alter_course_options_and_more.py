# Generated by Django 5.1.1 on 2024-09-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_alter_song_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesscode',
            options={'ordering': ('-course__name', 'code'), 'verbose_name_plural': 'Access Codes'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-name', '-year')},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ('-course__name', 'album__name', 'name')},
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]