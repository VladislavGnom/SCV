from django.core.exceptions import ValidationError

from quiz.models import AnswerOption


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