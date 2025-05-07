from django.test import TestCase
from quiz.forms import TestForm
from quiz.models import Test, Question, Answer


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
        self.ans1_1 = Answer.objects.create(
            question=self.q1,
            text='Correct',
            is_correct=True,
        )
        self.ans1_2 = Answer.objects.create(
            question=self.q1,
            text='Incorrect',
            is_correct=False,
        )
        self.ans2_1 = Answer.objects.create(
            question=self.q2,
            text='Correct',
            is_correct=True,
        )
        self.ans2_2 = Answer.objects.create(
            question=self.q2,
            text='Incorrect',
            is_correct=False,
        )


    def test_valid_form(self):
        form_data = {
            f'question_{self.q1.pk}': self.ans1_1,
            f'question_{self.q2.pk}': self.ans2_2,
        }
        form = TestForm(data=form_data, questions=self.test.questions.all())
        self.assertTrue(form.is_valid())

