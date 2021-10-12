from django.contrib import admin

from . import models


admin.site.register(models.Course)
admin.site.register(models.Song)
admin.site.register(models.Assignment, models.AssignmentAdmin)
admin.site.register(models.Homework, models.HomeworkAdmin)

admin.site.site_header = "learn-music administration"
