import functools
import urllib.parse as urlparse


from django.db.models import Count
from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponseServerError

from .forms import ConfigForm, LoginForm
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
    cards = []
    default_img_url = (
        "https://cdn4.iconfinder.com/data/icons/common-toolbar/36/Help-2-512.png"
    )
    for course in models.Course.objects.all():
        description = course.description
        if not description:
            num_homeworks = models.Homework.objects.filter(course=course).count()
            description = f"{num_homeworks} Homework{'s' if num_homeworks > 1 else ''}"
        cards.append(
            {
                "image_url": course.image_url or default_img_url,
                "description": description,
                "name": course.name,
                "url": reverse("courses:homeworks", kwargs={"code": course.code}),
                "link_text": course.code.upper(),
            }
        )
    return render(
        request,
        "courses/courses.html",
        {
            "title": "Check our awesome courses",
            "subtitle": "We may have the best music education",
            "cards": cards,
            "null_link": reverse("courses:index"),
        },
    )


@verify
def albums(request, code):
    try:
        course = models.Course.objects.get(code=code)
    except models.Course.DoesNotExist:
        return HttpResponseServerError()

    cards = []
    album_ids = (
        models.Song.objects.filter(course=course)
        .values_list("album__id", flat=True)
        .distinct()
    )
    default_img_url = (
        "https://cdn0.iconfinder.com/data/icons/music-231/48/Music-02-512.png"
    )
    for album in models.Album.objects.filter(id__in=album_ids):
        description = album.description
        if not description:
            num_songs = models.Song.objects.filter(album=album).count()
            description = f"{num_songs} Song{'s' if num_songs > 1 else ''}"
        cards.append(
            {
                "image_url": album.image_url or default_img_url,
                "description": description,
                "name": album.name,
                "url": reverse(
                    "courses:songs", kwargs={"code": code, "album_name": album.name}
                ),
                "link_text": album.name,
            }
        )

    return render(
        request,
        "courses/albums.html",
        {
            "title": f"Check the awesome album{'s' if len(cards) > 1 else ''} of {course.name}",
            "subtitle": None,
            "cards": cards,
            "null_link": reverse("courses:index"),
        },
    )


@verify
def songs(request, code, album_name):
    try:
        course = models.Course.objects.get(code=code)
    except models.Course.DoesNotExist:
        return HttpResponseServerError()

    aggregation = (
        models.Assignment.objects.values("song__id")
        .annotate(number_of_practices=Count("id"))
        .filter(
            homework__course=course,
            song__name__isnull=False,
            song__album__name=album_name,
        )
        .order_by("-number_of_practices")
    )

    songs = []
    for aggr in aggregation:
        song = {
            "song": models.Song.objects.get(id=aggr["song__id"]),
            "number_of_practices": aggr["number_of_practices"],
        }
        songs.append(song)

    return render(
        request,
        "courses/songs.html",
        {
            "songs": songs,
            "course": course,
        },
    )


@verify
def homeworks(request, code):
    try:
        course = models.Course.objects.get(code=code)
    except models.Course.DoesNotExist:
        return HttpResponseServerError()

    flip_order_by_name = request.session.get(f"{code}_flip_order_by_name", False)

    if flip_order_by_name:
        order_by = "-name"
    else:
        order_by = "name"

    cards = []
    default_img_url = "https://cdn3.iconfinder.com/data/icons/flat-office-icons-1/140/Artboard_1-10-512.png"
    for homework in (
        models.Homework.objects.filter(course=course).order_by(order_by).all()
    ):
        description = homework.description
        if not description:
            num_assignments = models.Assignment.objects.filter(
                homework=homework
            ).count()
            description = (
                f"{num_assignments} Assignment{'s' if num_assignments > 1 else ''}"
            )
        cards.append(
            {
                "image_url": homework.image_url or default_img_url,
                "description": description,
                "name": homework.name.capitalize(),
                "url": reverse(
                    "courses:assignments",
                    kwargs={"code": course.code, "name": homework.name},
                ),
                "link_text": homework.name.capitalize(),
            }
        )

    return render(
        request,
        "courses/homeworks.html",
        {
            "title": course.name,
            "subtitle": None,
            "cards": cards,
            "null_link": reverse("courses:courses"),
            "config_url": reverse("courses:config", kwargs={"code": course.code}),
            "albums_url": reverse("courses:albums", kwargs={"code": course.code}),
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


@verify
def config(request, code):
    if request.method == "POST":
        form = ConfigForm(request.POST)

        if form.is_valid():
            flip_order_by_name = form.cleaned_data.get("flip_order_by_name")
            request.session[f"{code}_flip_order_by_name"] = flip_order_by_name

            request.session.modified = True

        return redirect(reverse("courses:homeworks", kwargs={"code": code}))

    data = {
        "flip_order_by_name": request.session.get(f"{code}_flip_order_by_name", False),
    }
    form = ConfigForm(data)

    return render(
        request,
        "courses/config.html",
        {"form": form, "code": code},
    )
