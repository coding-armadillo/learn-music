# Generated by Django 4.1.7 on 2023-03-25 23:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0012_alter_accesscode_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homework",
            name="description",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]