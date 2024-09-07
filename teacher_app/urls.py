from django.urls import path
from . import views


urlpatterns = [
    path('add_task', views.add_task, name='add-task'),
    path('add_test', views.add_test, name='add-test'),
    path('my_classes', views.show_classes, name='show-classes'),
    path('show_tests/<int:class_id>', views.show_tests, name='show-tests'),
    path('show_result_detail/<int:class_id>/<title>', views.show_result_detail, name='show-result-detail'),
]
