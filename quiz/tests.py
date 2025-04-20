from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Test

class TestModelTestCase(TestCase):
    def test_exam_requires_time_limit(self):
        exam = Test(
            title="Экзамен",
            test_type=Test.TestType.EXAM,
            time_limit=None  # Нарушение правила
        )
        with self.assertRaises(ValidationError):
            exam.full_clean()