from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Song)
admin.site.register(models.Assignment, models.AssignmentAdmin)
admin.site.register(models.Homework, models.HomeworkAdmin)
