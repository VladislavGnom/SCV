from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from quiz.models import Test, Question, UserAnswer, UserTestResult, Answer
from quiz.utils import get_right_handler

User = get_user_model()


class UserAnswerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.test = Test.objects.create(title='Sample Test', test_type=Test.TestType.QUIZ)
        self.question = Question.objects.create(
            test=self.test,
            text='What is Django?',
            question_type=Question.QuestionType.TEXT_AUTO,
            correct_answer='Web framework'
        )
        self.test_result = UserTestResult.objects.create(
            user=self.user,
            test=self.test,
            completed_at=timezone.now()
        )

    def test_text_answer_auto_check_valid_data(self):
        '''Check auto checkup of text answer - valid data'''
        answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=self.question,
            text_answer='Web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )

        auto_check_answer = get_right_handler(self.question)
        auto_check_answer(self.question, answer)
    
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.score, self.question.max_score)
    
    def test_text_answer_auto_check_no_valid_data(self):
        '''Check auto checkup of text answer - no valid data'''
        answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=self.question,
            text_answer='Django is a web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )

        auto_check_answer = get_right_handler(self.question)
        auto_check_answer(self.question, answer)
    
        self.assertTrue(not answer.is_correct)
        self.assertEqual(answer.score, 0)

    def test_text_answer_auto_check_valid_data(self):
        '''Check auto checkup of text answer - valid data'''
        answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=self.question,
            text_answer='Web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )

        auto_check_answer = get_right_handler(self.question)
        auto_check_answer(self.question, answer)
    
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.score, self.question.max_score)

    def test_m2m_answer_creation(self):
        '''Check creation answer with selecting choices'''
        answer1 = Answer.objects.create(question=self.question, text='Correct', is_correct=True)
        answer2 = Answer.objects.create(question=self.question, text='Wrong', is_correct=False)

        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=self.question
        )
        user_answer.selected_answers.set([answer1])

        self.assertEqual(user_answer.selected_answers.count(), 1)
        self.assertEqual(user_answer.selected_answers.first(), answer1)


