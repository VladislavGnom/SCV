# # quiz/urls.py
# from django.urls import path
# from . import views
# from django.contrib.auth.decorators import login_required

# urlpatterns = [
#     # Основные пути
#     path('', views.TestListView.as_view(), name='test_list'),
#     # path('create/', login_required(views.TestCreateView.as_view()), name='test_create'),
#     path('<int:pk>/', views.TestDetailView.as_view(), name='test_detail'),
#     # path('<int:pk>/edit/', login_required(views.TestUpdateView.as_view()), name='test_update'),
#     # path('<int:pk>/delete/', login_required(views.TestDeleteView.as_view()), name='test_delete'),
    
#     # # Прохождение теста
#     # path('<int:test_id>/start/', login_required(views.TestStartView.as_view()), name='test_start'),
#     # path('<int:test_id>/submit/', login_required(views.TestSubmitView.as_view()), name='test_submit'),
#     # path('results/<int:result_id>/', login_required(views.TestResultView.as_view()), name='test_result'),
    
#     # # Вопросы и ответы (CRUD)
#     path('<int:test_id>/questions/add/', 
#     #      login_required(views.QuestionCreateView.as_view()), 
#     #      name='question_create'),
#     # path('questions/<int:pk>/edit/', 
#     #      login_required(views.QuestionUpdateView.as_view()), 
#     #      name='question_update'),
#     # path('questions/<int:pk>/delete/', 
#     #      login_required(views.QuestionDeleteView.as_view()), 
#     #      name='question_delete'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import test_view, TestStatisticsView, test_result_view, student_statistics

# router = DefaultRouter()
# router.register(r'tests', TestViewSet, basename='test')

urlpatterns = [
    path('user-test/<int:test_id>/', test_view, name='test-main'),
    path('handle-test/<int:test_id>/', test_view, name='submit-test'),
    path('test-statistics/', TestStatisticsView.as_view(), name='test-statistics'),
    path('my-statistics/', student_statistics, name='student_statistics'),
    path('test-result/<int:test_id>', test_result_view, name='test-result'),
    # path('api/', include(router.urls)),
]