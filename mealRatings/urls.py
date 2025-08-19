from django.urls import path
from . import views

app_name = "meals"
urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category>/", views.categoryList, name="category"),
    path("meal/<int:pk>/", views.detail, name="detail"),
]
