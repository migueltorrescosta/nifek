from django.shortcuts import render


def home(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, "home.html", context={})
