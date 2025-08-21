from django.urls import path
from . import views

app_name = "analisis"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("histograma/", views.histograma, name="histograma"),
]