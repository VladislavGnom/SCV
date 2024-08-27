from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('scv', views.scv_home, name='scv-home'),
    path('show_result', views.show_result, name='show-result'),
    path('refresh', views.refresh_func, name='refresh'),
    path('profile', views.profile, name='profile'),
    path('add_task', views.add_task, name='add-task'),
    path('add_test', views.add_test, name='add-test'),
    path('my_classes', views.show_classes, name='show-classes'),
    path('show_tests/<int:class_id>', views.show_tests, name='show-tests'),
    path('show_result_detail/<int:class_id>/<title>', views.show_result_detail, name='show-result-detail'),
]
