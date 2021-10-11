from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "contact_us/",
        views.contact_us,
        name="contact_us",
    ),
    path(
        "courses/",
        views.courses,
        name="courses",
    ),
    path(
        "course/<str:code>/",
        views.homeworks,
        name="homeworks",
    ),
    path(
        "course/<str:code>/<str:name>",
        views.assignments,
        name="assignments",
    ),
]
