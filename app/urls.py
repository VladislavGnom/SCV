from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('scv', views.scv_home, name='scv-home'),
    path('show_result', views.show_result, name='show-result'),
    path('refresh', views.refresh_func, name='refresh'),
]
