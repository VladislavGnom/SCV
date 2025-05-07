from django import forms

QUESTION_TYPES = {
    'single_choice': {
        'form_class': forms.RadioSelect,
        'template': 'quiz/questions/single_choice.html',
        'evaluation': lambda question, answer: question.options.filter(
            id=answer, is_correct=True
        ).exists()
    },
    'multiple_choice': {
        'form_class': forms.CheckboxSelectMultiple,
        'template': 'quiz/questions/multiple_choice.html',
        'evaluation': lambda question, answers: set(answers) == set(
            question.options.filter(is_correct=True).values_list('id', flat=True)
        )
    },
    'text_answer': {
        'form_class': forms.Textarea,
        'template': 'quiz/questions/text_answer.html',
        'evaluation': lambda question, answer: any(
            answer.lower() == opt.text.lower() 
            for opt in question.options.filter(is_correct=True)
        )
    }
}