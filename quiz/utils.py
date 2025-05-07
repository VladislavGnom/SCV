from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from quiz.models import Group as TestGroup, Test, Answer, Question, UserAnswer, UserTestResult
from quiz.services import check_text_answer, get_right_handler

User = get_user_model()

def prepare_answer_data(question, answer_data):
    """Подготавливает данные для сохранения UserAnswer"""
    data = {}
    
    if question.question_type in [Question.QuestionType.SINGLE, Question.QuestionType.MULTIPLE]:
        # Для вопросов с выбором ответа
        data['selected_answers'] = list(answer_data) if answer_data else []
        
    elif question.question_type in [Question.QuestionType.TEXT, Question.QuestionType.TEXT_AUTO]:
        # Для текстовых ответов
        data['text_answer'] = answer_data
        data['check_status'] = (
            UserAnswer.CheckStatusChoices.NEEDS_REVIEW 
            if question.question_type == Question.QuestionType.TEXT 
            else UserAnswer.CheckStatusChoices.AUTO_CHECKED
        )
    
    return data

def get_test_group_by_user(user: User):
    '''Return TestGroup instance if user has a group otherwise None'''
    return user.learning_groups.first()


def normilize_user_answers(user_questions_data: dict[str: str]):
    '''Normilizing the user's data of questions && Bring values of answers by questions'''
    normilized_user_questions_data = user_questions_data.copy()

    for question, value in normilized_user_questions_data.items():
        question_pk = question.split('_')[-1]
        question_obj = Question.objects.get(pk=question_pk)

        if isinstance(value, QuerySet):
            answers = [value[i].pk for i in range(len(value))]
            # here can be any normilization of the answers
            normilized_user_questions_data[question] = set(answers)
        else:
            if question_obj.question_type == question_obj.QuestionType.SINGLE:
                answer = [value.pk]
            else:
                answer = value

            normilized_user_questions_data[question] = answer

    return normilized_user_questions_data

def evaluate_answers_by_test(test: Test, user_questions_data: dict[str: str], test_result: UserTestResult) -> int:
    '''Evaluated answer of the questions 
    and defines the score for each question into UserAnswer models

    ''' 
    questions = test.questions.all()
    normilized_user_questions_data = normilize_user_answers(user_questions_data)

    for question in questions:
        question_key = f'question_{question.pk}'
        answer_data = normilized_user_questions_data.get(question_key)

        user_answer, created = UserAnswer.objects.update_or_create(
            user_test_result=test_result,
            question=question,
            defaults={
                'text_answer': answer_data if question.question_type in [Question.QuestionType.TEXT, Question.QuestionType.TEXT_AUTO] else None,
                'check_status': (
                    UserAnswer.CheckStatusChoices.NEEDS_REVIEW 
                    if question.question_type == Question.QuestionType.TEXT 
                    else UserAnswer.CheckStatusChoices.AUTO_CHECKED
                )
            }
        )

        # Устанавливаем M2M-связи отдельно
        if question.question_type in [Question.QuestionType.SINGLE, Question.QuestionType.MULTIPLE]:
            # assert 1 == 0, answer_data
            user_answer.selected_answers.set(answer_data if answer_data else [])

        auto_check_answer = get_right_handler(question)
        auto_check_answer(question, user_answer)
        
    return True
