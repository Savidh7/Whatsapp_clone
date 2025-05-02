from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('users/', views.user_list, name='user_list'),
    path('messages/<str:username>/', views.get_messages, name='get_messages'),
]