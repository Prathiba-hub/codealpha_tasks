from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

    path('profile/<int:user_id>/', views.profile, name='profile'),

    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),

]