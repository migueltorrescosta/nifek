from . import views
from django.urls import path

app_name = "hold"

urlpatterns = [
    path("", views.home, name="home"),
    path("e/", views.post_entity, name="entity"),
    path("s/", views.post_stake, name="stake"),
    path("e/<int:pk>/", views.EntityDetail.as_view(), name="entity_detail"),
]
