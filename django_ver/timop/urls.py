from django.urls import path
from . import views


urlpatterns = [
    path('', views.timop, name='timop'),
    path('about/', views.about, name='timop-about')
]
