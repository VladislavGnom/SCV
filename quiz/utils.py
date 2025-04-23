from django.contrib.auth import get_user_model
from quiz.models import Group as TestGroup, Test, Answer

User = get_user_model()

def get_test_group_by_user(user: User):
    '''Return TestGroup instance if user has a group otherwise None'''
    return user.learning_groups.first()


def normilize_user_answers(user_questions_data: dict[str: str]):
    '''Normilizing the user's data of questions && Bring values of answers by questions'''
    normilized_user_questions_data = user_questions_data.copy()

    for question, value in normilized_user_questions_data.items():
        if isinstance(value, list):
            answers = [Answer.objects.get(pk=value[i]).text for i in range(len(value))]
            # here can be any normilization of the answers
            normilized_user_questions_data[question] = set(answers)
        else:
            answer = Answer.objects.get(pk=value).text

            normilized_user_questions_data[question] = answer

    return normilized_user_questions_data

def calculate_scores_by_test(test: Test, user_questions_data: dict[str: str]) -> int:
    '''Calculated scores for the test and return its'''
    questions = test.questions.all()
    normilized_user_questions_data = normilize_user_answers(user_questions_data)
    scores = 0

    for qs in questions:
        question_key = f'question_{qs.pk}'
        
        if qs.question_type == qs.QuestionType.SINGLE:
            right_answer = qs.answers.get(is_correct=True).text
        elif qs.question_type == qs.QuestionType.MULTIPLE:
            right_answer = set([answer.text for answer in qs.answers.filter(is_correct=True)])

        user_answer = normilized_user_questions_data.get(question_key)

        if user_answer == right_answer:
            scores += 1    # TODO: make separate score by every question
        
    return scores

        