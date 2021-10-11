from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.code.upper()


class Song(models.Model):
    name = models.CharField(max_length=200)
    upload = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.course}-{self.name}"


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(
        max_length=200,
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

    def __str__(self):
        return f"{self.homework}-{self.name}"
