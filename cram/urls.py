from . import views
from django.urls import path

app_name = "cram"

urlpatterns = [
    path("", views.home, name="home"),
    path("review", views.review, name="review"),
    path("collections", views.CollectionListView.as_view(), name="collections"),
    path(
        "collections/<int:pk>/",
        views.CollectionDetail.as_view(),
        name="collection_detail",
    ),
    path(
        "submit_review/<int:pk>/",
        views.UserCardScoreDetailView.as_view(),
        name="submit_review",
    ),
]
