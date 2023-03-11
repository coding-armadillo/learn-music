from django.contrib import admin
from django.db import models
from tinymce.models import HTMLField


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ("-name",)

    def __str__(self):
        return self.code.upper()


class Album(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Song(models.Model):
    name = models.CharField(max_length=200)
    upload = models.FileField(upload_to="uploads/")
    gala_piece = models.BooleanField(default=False)
    solfege = models.TextField(blank=True, null=True)

    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class SongAdmin(admin.ModelAdmin):
    list_filter = (
        ("course", admin.RelatedFieldListFilter),
        ("album", admin.RelatedFieldListFilter),
    )


class Homework(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = (
            "-course__name",
            "-name",
        )

    def __str__(self):
        return f"{self.course}-{self.name}"


class HomeworkAdmin(admin.ModelAdmin):
    list_filter = (("course", admin.RelatedFieldListFilter),)

    def get_changeform_initial_data(self, request):
        homework = Homework.objects.all().order_by("-course__code", "-name").first()
        name = homework.name
        try:
            number = str(int(name[-2:]) + 1).zfill(2)
        except:
            number = ""
        course = homework.course
        return {"name": f"Homework{number}", "course": course}


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    text = HTMLField(
        max_length=800,
        blank=True,
        null=True,
    )
    song = models.ForeignKey(
        "Song",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    homework = models.ForeignKey(
        "Homework",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = (
            "-homework__course__name",
            "-homework__name",
            "-name",
        )

    def __str__(self):
        return f"{self.homework}-{self.name}"


class AssignmentAdmin(admin.ModelAdmin):
    list_filter = (("homework", admin.RelatedFieldListFilter),)

    def get_changeform_initial_data(self, request):
        assignment = (
            Assignment.objects.all()
            .order_by("-homework__course__code", "-homework__name", "-name")
            .first()
        )
        name = assignment.name
        try:
            number = str(int(name[-2:]) + 1).zfill(2)
        except:
            number = ""
        homework = assignment.homework
        return {"name": f"Assignment{number}", "homework": homework}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "homework":
            kwargs["queryset"] = Homework.objects.all().order_by(
                "-course__code", "-name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccessCode(models.Model):
    code = models.CharField(max_length=50)
    student = models.CharField(max_length=50)
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("course__name", "code")
        unique_together = ["course", "code"]

    def __str__(self):
        return f"{self.course}-{self.student}"
