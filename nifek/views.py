from django.shortcuts import render


def home(request):
    """View function for home page of site."""

    context = {
        "thes_tags": ["forecasting", "truth", "accountability"],
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "home.html", context=context)
