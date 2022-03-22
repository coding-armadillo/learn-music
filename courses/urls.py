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
        "albums/<str:code>/",
        views.albums,
        name="albums",
    ),
    path(
        "songs/<str:code>/<str:album_name>/",
        views.songs,
        name="songs",
    ),
    path(
        "homeworks/<str:code>/",
        views.homeworks,
        name="homeworks",
    ),
    path(
        "assignments/<str:code>/<str:name>/",
        views.assignments,
        name="assignments",
    ),
    path(
        "login/",
        views.login,
        name="login",
    ),
    path(
        "logout/",
        views.logout,
        name="logout",
    ),
    path(
        "config/<str:code>/",
        views.config,
        name="config",
    ),
]
