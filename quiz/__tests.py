from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from quiz.models import Test, Question, Answer
from quiz.forms import AnswerInlineFormSet

User = get_user_model()

class TestValidation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin',
            password='password',
            email='admin@example.com'
        )
        cls.client = Client()
        cls.client.login(username='admin', password='password')

    def test_single_choice_validation(self):
        """Тест валидации вопроса с одним правильным ответом"""
        test = Test.objects.create(title="Validation Test")
        url = reverse('admin:quiz', args=[test.id])
        
        # Данные формы с 2 ответами (оба правильные - должно быть ошибка)
        data = {
            'title': 'Validation Test',
            'question_set-TOTAL_FORMS': '1',
            'question_set-INITIAL_FORMS': '0',
            'question_set-0-text': 'Sample Question',
            'question_set-0-question_type': Question.QuestionType.SINGLE,
            'question_set-0-answer_set-TOTAL_FORMS': '2',
            'question_set-0-answer_set-INITIAL_FORMS': '0',
            'question_set-0-answer_set-0-text': 'Answer 1',
            'question_set-0-answer_set-0-is_correct': 'on',
            'question_set-0-answer_set-1-text': 'Answer 2',
            'question_set-0-answer_set-1-is_correct': 'on',
        }
        
        response = self.client.post(url, data)
        self.assertContains(response, "должен быть ровно один правильный вариант")

    def test_multiple_choice_validation(self):
        """Тест валидации вопроса с несколькими ответами"""
        test = Test.objects.create(title="Validation Test")
        url = reverse('admin:quiz_test_change', args=[test.id])
        
        # Данные формы без правильных ответов - должно быть ошибка
        data = {
            'title': 'Validation Test',
            'question_set-TOTAL_FORMS': '1',
            'question_set-INITIAL_FORMS': '0',
            'question_set-0-text': 'Sample Question',
            'question_set-0-question_type': Question.QuestionType.MULTIPLE,
            'question_set-0-answer_set-TOTAL_FORMS': '2',
            'question_set-0-answer_set-INITIAL_FORMS': '0',
            'question_set-0-answer_set-0-text': 'Answer 1',
            'question_set-0-answer_set-1-text': 'Answer 2',
        }
        
        response = self.client.post(url, data)
        self.assertContains(response, "нужно выбрать хотя бы один правильный вариант")

    def test_min_answers_validation(self):
        """Тест валидации минимального количества ответов"""
        test = Test.objects.create(title="Validation Test")
        url = reverse('admin:your_app_test_test_change', args=[test.id])
        
        # Данные формы с 1 ответом - должно быть ошибка
        data = {
            'title': 'Validation Test',
            'question_set-TOTAL_FORMS': '1',
            'question_set-INITIAL_FORMS': '0',
            'question_set-0-text': 'Sample Question',
            'question_set-0-question_type': Question.QuestionType.SINGLE,
            'question_set-0-answer_set-TOTAL_FORMS': '1',
            'question_set-0-answer_set-INITIAL_FORMS': '0',
            'question_set-0-answer_set-0-text': 'Only Answer',
            'question_set-0-answer_set-0-is_correct': 'on',
        }
        
        response = self.client.post(url, data)
        self.assertContains(response, "минимум 2 ответа")

# TODO 
# class AnswerFormSetTest(TestCase):
#     def test_formset_validation(self):
#         """Тест валидации FormSet напрямую"""
#         test = Test.objects.create(title="Validation Test")

#         question = Question.objects.create(
#             text="Test Question",
#             question_type=Question.QuestionType.SINGLE,
#             test=test
#         )
        
#         # Создаем FormSet с 2 правильными ответами
#         formset_data = {
#             'form-TOTAL_FORMS': '2',
#             'form-INITIAL_FORMS': '0',
#             'form-0-text': 'Answer 1',
#             'form-0-is_correct': 'on',
#             'form-1-text': 'Answer 2',
#             'form-1-is_correct': 'on',
#         }
        
#         formset = AnswerInlineFormSet(
#             data=formset_data,
#             instance=question
#         )
        
#         self.assertFalse(formset.is_valid())
#         self.assertIn(
#             "должен быть ровно один правильный вариант",
#             str(formset.non_form_errors())
#         )