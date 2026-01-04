from django.urls import path
from .views import login_user, register_user, logout_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
