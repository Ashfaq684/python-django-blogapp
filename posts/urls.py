from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/update/', views.update_post, name='update_post'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('tag/all_posts/<slug:slug>', views.tag_all_posts, name='tag_all_posts'),
    path('bookmark_post/<slug:slug>', views.bookmark_post, name='bookmark_post'),
    path('like_post/<slug:slug>', views.like_post, name='like_post'),
    path('all_bookmarked_posts/', views.all_bookmarked_posts, name='all_bookmarked_posts'),
    path('all_liked_posts/', views.all_liked_posts, name='all_liked_posts'),
]
