from django.db.models import Count
from django.shortcuts import render
from django.http.response import HttpResponseServerError

from . import models


def index(request):
    return render(request, "courses/index.html")


def courses(request):
    return render(
        request,
        "courses/courses.html",
        {
            "courses": models.Course.objects.all(),
        },
    )


def songs(request, code):
    try:
        course = models.Course.objects.get(code=code)
    except models.Course.DoesNotExist:
        return HttpResponseServerError()

    return render(
        request,
        "courses/songs.html",
        {
            "songs": (
                models.Assignment.objects.values("song__name")
                .annotate(number_of_practices=Count("id"))
                .order_by()
                .filter(
                    homework__course=course,
                    song__name__isnull=False,
                )
            ),
            "course": course,
        },
    )


def homeworks(request, code):
    try:
        course = models.Course.objects.get(code=code)
    except models.Course.DoesNotExist:
        return HttpResponseServerError()

    return render(
        request,
        "courses/homeworks.html",
        {
            "homeworks": models.Homework.objects.filter(course=course)
            .order_by("name")
            .all(),
            "course": course,
        },
    )


def assignments(request, code, name):
    try:
        homework = models.Homework.objects.get(course__code=code, name=name)
    except models.homework.DoesNotExist:
        return HttpResponseServerError()

    return render(
        request,
        "courses/assignments.html",
        {
            "assignments": models.Assignment.objects.filter(homework=homework)
            .order_by("name")
            .all(),
            "homework": homework,
        },
    )


def contact_us(request):
    return render(request, "courses/contact_us.html")
