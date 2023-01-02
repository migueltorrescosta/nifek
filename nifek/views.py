from django.shortcuts import render
from django.urls import reverse


def home(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    apps = [
        {
            "title": "💡 Thes",
            "description": "A record of thoughts and ideas.",
            "url": reverse("thes:home"),
        },
        {
            "title": "💼 Hold",
            "description": "Tracker for company ownership.",
            "url": reverse("hold:home"),
        },
    ]
    return render(request, "home.html", context={"apps": apps})
