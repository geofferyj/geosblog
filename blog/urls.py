from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='blog_index'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:slug>/', views.TagIndexView.as_view(), name='tag')
]
