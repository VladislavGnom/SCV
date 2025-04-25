from django.contrib.auth import get_user_model
from quiz.models import Group as TestGroup, Test, Answer, Question
from quiz.services import check_text_answer, get_right_handler

User = get_user_model()

def get_test_group_by_user(user: User):
    '''Return TestGroup instance if user has a group otherwise None'''
    return user.learning_groups.first()


def normilize_user_answers(user_questions_data: dict[str: str]):
    '''Normilizing the user's data of questions && Bring values of answers by questions'''
    normilized_user_questions_data = user_questions_data.copy()

    for question, value in normilized_user_questions_data.items():
        question_pk = question.split('_')[-1]
        question_obj = Question.objects.get(pk=question_pk)

        if isinstance(value, list):
            answers = [Answer.objects.get(pk=value[i]).text for i in range(len(value))]
            # here can be any normilization of the answers
            normilized_user_questions_data[question] = set(answers)
        else:
            if value.isdigit() and question_obj.question_type == question_obj.QuestionType.SINGLE:
                answer = Answer.objects.get(pk=value).text
            else:
                answer = value

            normilized_user_questions_data[question] = answer

    return normilized_user_questions_data

def calculate_scores_by_test(test: Test, user_questions_data: dict[str: str]) -> int:
    '''Calculated scores for the test and return its'''
    questions = test.questions.all()
    normilized_user_questions_data = normilize_user_answers(user_questions_data)
    scores = 0

    for question in questions:
        question_key = f'question_{question.pk}'
        user_answer = normilized_user_questions_data.get(question_key)

        check_func = get_right_handler(question)
        if check_func(question, user_answer):
            scores += question.max_score
        
    return scores

        