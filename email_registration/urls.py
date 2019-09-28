from django.urls import path

from . import views

app_name = "email_registration"

urlpatterns = [
    path("", views.email_registration_form, name="email_registration_form"),
    path("<code>/", views.email_registration_confirm, name="email_registration_confirm"),
]
