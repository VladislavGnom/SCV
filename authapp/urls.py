from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # post views
    # path('login/', auth_views.LoginView.as_view(template_name='authapp/login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authapp/logout.html'), name='logout'),
]