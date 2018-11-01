import datetime
from django.shortcuts import render

from .models import Weather


def index(request):
    return render(
        request,
        "index.html",
        {"last_updated": datetime.datetime.now(), "weathers": Weather.objects.all()},
    )
