from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('scv', views.scv_home, name='scv-home'),
    path('show_result', views.show_result, name='show-result'),
    path('refresh', views.refresh_func, name='refresh'),
    path('profile', views.profile, name='profile'),
    path('user_test/<int:user_test_id>', views.user_test, name='user-test'),
    path('profile/show_tests_user', views.show_tests_user_profile, name='show-tests-user-profile'),
]
