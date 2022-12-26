# accounts/urls.py
from django.urls import path
from .views import EditProfile

app_name = "accounts"

urlpatterns = [
    path("profile", EditProfile.as_view(), name="profile"),
]
