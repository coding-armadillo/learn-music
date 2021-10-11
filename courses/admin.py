from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Song)
admin.site.register(models.Assignment)
admin.site.register(models.Homework)
