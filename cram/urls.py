from django.urls import path

from . import views

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
    path(
        "collections/<int:pk>/star",
        views.star_collection,
        name="star_collection",
    ),
    path(
        "collections/<int:pk>/unstar",
        views.unstar_collection,
        name="unstar_collection",
    ),
]
