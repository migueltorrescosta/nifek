from . import views
from django.urls import path

app_name = "hold"

urlpatterns = [
    path("", views.home, name="home"),
    path("e/<int:pk>/", views.EntityDetail.as_view(), name="entity_detail"),
]
