from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_api_home, name='test-api-home'),
]
