from django.core.exceptions import ValidationError

def validate_test_type(test):
    '''Проверяет логическую согласованность типа теста'''
    if test.test_type == test.TestType.EXAM and not test.time_limit:
        raise ValidationError(
            'Экзамен должен иметь лимит времени',
            params={'test_type': test.test_type}
        )