from django.urls import path
from . import views


urlpatterns = [
    path('tests', views.tests_page, name='show-tests'),
    path('add_task', views.add_task, name='add-task'),
    path('add_test', views.add_test, name='add-test'),
    path('add_test/<int:subject_main_id>/', views.add_task_subject, name='subject-main'),
    path('add_testq/<int:subject_main_id>/<int:question_id>/', views.add_task_question_safe, name='question-safe'),
    path('add_test/<int:subject_main_id>/<int:subject_parent_id>/', views.add_task_subject_parents, name='subject-parents'),
    path('add_test/<int:subject_main_id>/<int:subject_parent_id>/<int:subject_children_id>/', views.add_task_subject_children, name='subject-children'),
    path('add_test/<int:subject_main_id>/<int:subject_parent_id>/<int:subject_children_id>/<int:question_id>/', views.add_task_question, name='question'),
    path('my_classes', views.show_classes, name='show-classes'),
    path('show_tests/<int:class_id>', views.show_tests, name='show-tests'),
    path('show_result_detail/<int:class_id>/<title>', views.show_result_detail, name='show-result-detail'),
    path('show_user_images/<int:class_id>', views.show_user_images, name='show-user-images'),
    path('show_data_users/<int:class_id>', views.show_data_users, name='show-data-users'),

    # links for new pages of new types tests - UPDATE
    path('add_test_new_format', views.add_test_new_format_view, name='add-test-new-format'),
]
