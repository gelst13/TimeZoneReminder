from django.urls import path
from . import views


urlpatterns = [
    path('', views.timez, name='timop-timez'),
    path('timop/', views.timop, name='timop-timop'),
    path('timop/<local_offset>', views.timop, name='timop-anon'),
    path('about/', views.about, name='timop-about')
]
