from django.urls import path
from . import views
from .views import ContactDetailView


urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('contact/<int:pk>', ContactDetailView.as_view(), name='contact-detail'),
]
