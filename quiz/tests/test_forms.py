from django.test import TestCase
from quiz.forms import TestForm
from quiz.models import Test, Question


class TestTestCaseForm(TestCase):
    def setUp(self):
        self.test = Test.objects.create(
            title='SampleTest'
        )
        self.q1 = Question.objects.create(
            test=self.test,
            text='Question #1'
        )
        self.q2 = Question.objects.create(
            test=self.test,
            text='Question #2'
        )


    def test_valid_form(self):
        form_data = {
            f'question_{self.q1.pk}': self.q1,
            f'question_{self.q2.pk}': self.q2,
        }
        form = TestForm(data=form_data, questions=self.test.questions.all())
        self.assertTrue(form.is_valid())

