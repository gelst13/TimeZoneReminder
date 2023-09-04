from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostUpdateView


urlpatterns = [
    # path('', views.blog, name='blog'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
