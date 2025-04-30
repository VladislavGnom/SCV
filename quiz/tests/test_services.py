from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from quiz.models import Question, UserAnswer, Test, Answer, UserTestResult
from quiz.services import check_single_answer, check_multiple_answer, check_auto_text_answer

User = get_user_model()

class ServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.test = Test.objects.create(
            title='Sample Test',
            test_type=Test.TestType.QUIZ
        )
        self.test_result = UserTestResult.objects.create(
            user=self.user,
            test=self.test,
            completed_at=timezone.now()
        )

    def test_check_single_answer(self):
        question = Question.objects.create(
            test=self.test,
            text='What is Django?',
            question_type=Question.QuestionType.SINGLE
        )
        answer1 = Answer.objects.create(
            question=question,
            text='Correct',
            is_correct=True
        )
        answer2 = Answer.objects.create(
            question=question,
            text='InCorrect',
            is_correct=False
        )
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question
        )
        # ----------- correct data ---------------
        user_answer.selected_answers.set([answer1])

        check_single_answer(question, user_answer)

        self.assertTrue(user_answer.is_correct)
        self.assertEqual(user_answer.score, question.max_score)
        # ----------------------------------------

        user_answer.selected_answers.clear()    # явно очищаем связи

        # ----------- incorrect data ---------------
        user_answer.selected_answers.set([answer2])

        check_single_answer(question, user_answer)

        self.assertTrue(not user_answer.is_correct)
        self.assertEqual(user_answer.score, 0)
        # ----------------------------------------

    def test_check_multiple_answer(self):
        question = Question.objects.create(
            test=self.test,
            text='What is Django?',
            question_type=Question.QuestionType.MULTIPLE
        )
        answer1 = Answer.objects.create(
            question=question,
            text='Correct#1',
            is_correct=True
        )
        answer2 = Answer.objects.create(
            question=question,
            text='InCorrect#1',
            is_correct=False
        )
        answer3 = Answer.objects.create(
            question=question,
            text='InCorrect#2',
            is_correct=False
        )
        answer4 = Answer.objects.create(
            question=question,
            text='Correct#2',
            is_correct=True
        )
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question
        )
        # ----------- correct data ---------------
        user_answer.selected_answers.set([answer1, answer4])

        check_multiple_answer(question, user_answer)

        self.assertTrue(user_answer.is_correct)
        self.assertEqual(user_answer.score, question.max_score)
        # ----------------------------------------

        user_answer.selected_answers.clear()    # явно очищаем связи

        # ----------- incorrect data ---------------
        # incorrect - incorrect answer check
        user_answer.selected_answers.set([answer2, answer3])

        check_multiple_answer(question, user_answer)

        self.assertTrue(not user_answer.is_correct)
        self.assertEqual(user_answer.score, 0)

        user_answer.selected_answers.clear()    # явно очищаем связи
        
        # correct - incorrect answer check
        user_answer.selected_answers.set([answer1, answer3])

        check_multiple_answer(question, user_answer)

        self.assertTrue(not user_answer.is_correct)
        self.assertEqual(user_answer.score, 0)
        # ----------------------------------------

    def test_check_text_auto_answer_fuzzy_match_off(self):
        question = Question.objects.create(
            test=self.test,
            text='What is Django?',
            question_type=Question.QuestionType.TEXT_AUTO,
            correct_answer='Web framework',
            answer_fuzzy_match=False
        )
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question,
            text_answer='Web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )
        # ----------- correct data ---------------
        check_auto_text_answer(question, user_answer)

        self.assertTrue(user_answer.is_correct)
        self.assertEqual(user_answer.score, question.max_score)
        # ----------------------------------------

        UserAnswer.objects.all().delete() # явно очищаем все ответы

        # ----------- incorrect data ---------------
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question,
            text_answer='Django is a web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )
        check_auto_text_answer(question, user_answer)

        self.assertTrue(not user_answer.is_correct)
        self.assertEqual(user_answer.score, 0)
        # ----------------------------------------

    def test_check_text_auto_answer_fuzzy_match_on(self):
        question = Question.objects.create(
            test=self.test,
            text='What is Django?',
            question_type=Question.QuestionType.TEXT_AUTO,
            correct_answer='Web framework',
            answer_fuzzy_match=True
        )
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question,
            text_answer='web framework!',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )
        # ----------- correct data ---------------
        check_auto_text_answer(question, user_answer)

        self.assertTrue(user_answer.is_correct)
        self.assertEqual(user_answer.score, question.max_score)
        # ----------------------------------------

        UserAnswer.objects.all().delete() # явно очищаем все ответы

        # ----------- incorrect data ---------------
        user_answer = UserAnswer.objects.create(
            user_test_result=self.test_result,
            question=question,
            text_answer='Django is a web framework',
            check_status=UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )
        check_auto_text_answer(question, user_answer)

        self.assertTrue(not user_answer.is_correct)
        self.assertEqual(user_answer.score, 0)
        # ----------------------------------------
