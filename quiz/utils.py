from django.contrib.auth import get_user_model
from quiz.models import Group as TestGroup

User = get_user_model()

def get_test_group_by_user(user: User):
    '''Return TestGroup instance if user has a group otherwise None'''
    return user.learning_groups.first()