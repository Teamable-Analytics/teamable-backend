from django.urls import path

from lti import views

urlpatterns = [
    path("login/", views.login),
    path("launch/", views.launch),
]
