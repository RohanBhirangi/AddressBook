from django.urls import path
from . import views

urlpatterns = [
    path("contact", views.contact, name="contact"),
    path("contact/<slug:name>", views.contact_name, name="contact_name")
]
