from . import views
from django.urls import path

urlpatterns = [
    path('', views.ThesisList.as_view(), name='home'),
    path('t/<int:pk>/', views.ThesisDetail.as_view(), name='thesis_detail'),
]
