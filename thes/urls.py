from django.urls import path

from . import views

app_name = "thes"

urlpatterns = [
    path("", views.ThesisList.as_view(), name="home"),
    path("thesis/<int:pk>/", views.ThesisDetail.as_view(), name="thesis_detail"),
    path("thesis/<int:pk>/tag/", views.TagThesisView.as_view(), name="tag_thesis"),
]
