from django.urls import path

from . import views

urlpatterns = [
    path('login/<int:id>', views.login),
]