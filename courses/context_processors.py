from django.conf import settings


def selected_settings(request):
    return {
        "VERSION": settings.VERSION,
    }
