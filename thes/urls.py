from . import views
from django.urls import path

app_name = "thes"

urlpatterns = [
    path("", views.ThesisList.as_view(), name="thes"),
    path("t/<int:pk>/", views.ThesisDetail.as_view(), name="thesis_detail"),
]
