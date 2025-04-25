from django.core.exceptions import ValidationError
from quiz.models import UserAnswer, Question


class TestEvaluator:
    def __init__(self, test, user_answers):
        self.test = test
        self.user_answers = user_answers
        self.results = {
            'total_score': 0,
            'max_score': sum(q.points for q in test.questions.all()),
            'questions': []
        }
    
    def evaluate(self):
        for question in self.test.questions.all():
            self._evaluate_question(question)
        return self.results
    
    def _evaluate_question(self, question):
        user_answer = self.user_answers.get(str(question.id))
        question_type = question.type.name
        
        evaluator = getattr(self, f'_evaluate_{question_type}', None)
        if not evaluator:
            raise ValidationError(f"Unknown question type: {question_type}")
        
        is_correct, feedback = evaluator(question, user_answer)
        
        question_result = {
            'id': question.id,
            'text': question.text,
            'is_correct': is_correct,
            'user_answer': user_answer,
            'feedback': feedback,
            'points': question.points if is_correct else 0
        }
        
        self.results['total_score'] += question_result['points']
        self.results['questions'].append(question_result)
    
    def _evaluate_single_choice(self, question, answer_id):
        try:
            option = question.options.get(id=answer_id)
            return option.is_correct, option.feedback or question.explanation
        except AnswerOption.DoesNotExist:
            return False, "Не выбран вариант ответа"
        
from difflib import SequenceMatcher
from quiz.models import Question
import re

def check_single_answer(question: Question, user_answer: UserAnswer):
    """
    Checking single answer
    """
    # Проверка одиночного выбора
    correct_answer = question.answers.filter(is_correct=True).first()
    user_answer.is_correct = (
        user_answer.selected_answers.count() == 1 and
        user_answer.selected_answers.first() == correct_answer
    )
    
    user_answer.save()

def check_multiple_answer(question: Question, user_answer: UserAnswer):
    """
    Checking multiple answer
    """
    # Проверка множественного выбора
    correct_ids = set(question.answers.filter(is_correct=True).values_list('id', flat=True))
    selected_ids = set(user_answer.selected_answers.values_list('id', flat=True))
    user_answer.is_correct = correct_ids == selected_ids
    
    user_answer.save()

def check_text_answer(question, user_answer):
    """
    Checking text answer
    """
    if question.question_type == Question.QuestionType.TEXT_AUTO:
        return check_auto_text_answer(question, user_answer)
    # TODO: реализовать проверку чисто текстовых ответов
    return None  # Для ручной проверки возвращаем None 

def check_auto_text_answer(question: Question, user_answer: UserAnswer):
    """
    Auto checking text answer
    """
    correct_answer = question.correct_answer.lower().strip()
    text_answer = user_answer.text_answer.lower().strip()
    
    if not question.answer_fuzzy_match:
        # Точное сравнение
        return correct_answer == user_answer
    
    if text_answer and correct_answer:
        # Нечеткое сравнение
        similarity = SequenceMatcher(None, correct_answer, text_answer).ratio()
        user_answer.is_correct = similarity >= 0.8
        user_answer.score = question.max_score if user_answer.is_correct else 0

    user_answer.save()

HANDLER_MAP = {
    'SN': check_single_answer,
    'ML': check_multiple_answer,
    'TX': check_text_answer,
    'TXA': check_text_answer
}

def get_right_handler(question):
    '''Map question types of handlers'''
    try:
        return HANDLER_MAP[question.question_type]
    except KeyError as error:
        raise KeyError(f'Not available type of test: {error}')