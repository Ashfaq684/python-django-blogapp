from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('profile/edit/<slug:slug>/', views.edit_profile, name='edit_profile'),
    path('author/<slug:slug>/', views.author_page, name='author_page'),
]
