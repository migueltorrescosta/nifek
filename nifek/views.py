import random

from django.shortcuts import render
from django.urls import reverse


def home(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    apps = [
        {
            "title": "💼 Hold",
            "description": "Following links of ownership through multiple corporations can be rather hard. Hold allows you to submit the ownership relations you know, and intuitively show you the full view of ownership links.",
            "url": reverse("hold:home"),
        },
        {
            "title": "💡 Thes",
            "description": "Thes allows you to store thoughts and beliefs, in an easily retrievable way.",
            "url": reverse("thes:home"),
        },
        {
            "title": "📓 Cram",
            "description": "Cram allows you to study more efficiently by using Spaced Repetition.",
            "url": reverse("cram:home"),
        },
    ]
    random.shuffle(apps)
    return render(request, "home.html", context={"apps": apps})
