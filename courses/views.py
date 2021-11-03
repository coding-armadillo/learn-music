import functools
import urllib.parse as urlparse


from django.db.models import Count
from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponseServerError

from .forms import LoginForm
from . import models


def update_query_string(url, params):
    parse_results = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(parse_results.query))

    query.update(params)

    parse_results = list(parse_results)
    parse_results[4] = urlparse.urlencode(query)
    url = urlparse.urlunparse(parse_results)

    return url


def verify(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        course_code = kwargs.get("code", None)
        homework_name = kwargs.get("name", None)
        if not course_code:
            return redirect(reverse("courses:index"))

        params = {"course": course_code}
        if homework_name:
            params["homework"] = homework_name

        logged_in = request.session.get(course_code, False)
        if not logged_in:
            return redirect(update_query_string(reverse("courses:login"), params))

        return func(*args, **kwargs)

    return wrapper


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            access_code = form.cleaned_data["access_code"]
            course_code = request.GET.get("course", None)
            homework_name = request.GET.get("homework", None)
            if not course_code:
                return redirect(reverse("courses:courses"))

            try:
                ac = models.AccessCode.objects.get(
                    code=access_code, course__code=course_code
                )
            except models.AccessCode.DoesNotExist:
                ac = None
            if ac is not None:
                request.session[course_code] = True

                if homework_name:
                    return redirect(
                        reverse(
                            "courses:assignments",
                            kwargs={"code": course_code, "name": homework_name},
                        )
                    )
                return redirect(
                    reverse("courses:homeworks", kwargs={"code": course_code})
                )

            return redirect(reverse("courses:courses"))

    form = LoginForm()
    return render(
        request,
        "courses/login.html",
        {"form": form},
    )


def logout(request):
    for course in models.Course.objects.all():
        request.session.pop(course.code, None)
    return redirect(reverse("courses:index"))


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


@verify
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


@verify
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


@verify
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
