from django.urls import path
from . import views
from .views import (ContactDetailView, ContactCreateView, ContactUpdateView,
                    ContactListView, ContactDeleteView)


urlpatterns = [
    # path('', views.contacts, name='contacts'),
    # path('', ContactListView.as_view(), name='contacts'),
    # path('contact/<str:username>', ContactListView.as_view(), name='user-contacts'),
    path('contact/<int:pk>', ContactDetailView.as_view(), name='contact-detail'),
    path('contact/new/', ContactCreateView.as_view(), name='contact-add'),
    path('contact/<int:pk>/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
]
