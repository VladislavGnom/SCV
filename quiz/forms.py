from django import forms
from quiz.models import Question


class AnswerInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        # Получаем все валидные и неудаленные формы ответов
        valid_forms = [
            form for form in self.forms 
            if form.is_valid() and not form.cleaned_data.get('DELETE', False)
        ]
        
        if not valid_forms:
            return
            
        # Получаем тип вопроса из родительской формы вопроса
        question_type = None
        
        # Способ 1: для новых вопросов (еще не сохраненных)
        if hasattr(self, 'parent_form') and hasattr(self.parent_form, 'cleaned_data'):
            question_type = self.parent_form.cleaned_data.get('question_type')
        # Способ 2: для существующих вопросов
        elif hasattr(self.instance, 'question'):
            question_type = self.instance.question.question_type
        
        if not question_type:
            return
            
        # Считаем количество правильных ответов
        correct_count = sum(
            1 for form in valid_forms 
            if form.cleaned_data.get('is_correct', False)
        )
        
        # Валидация по типу вопроса
        if question_type == Question.QuestionType.SINGLE and correct_count != 1:
            raise forms.ValidationError(
                "Для вопроса с одним ответом должен быть ровно один правильный вариант!"
            )
        elif question_type == Question.QuestionType.MULTIPLE and correct_count < 1:
            raise forms.ValidationError(
                "Для вопроса с несколькими ответами нужно выбрать хотя бы один правильный вариант!"
            )
        

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            if question.question_type == Question.QuestionType.SINGLE:
                self.fields[f'question_{question.pk}'] = forms.ChoiceField(
                    choices=[(a.pk, a.text) for a in question.answers.all()],
                    widget=forms.RadioSelect,
                    label=question.text,
                    required=True
                )
            elif question.question_type == Question.QuestionType.MULTIPLE:
                self.fields[f'question_{question.pk}'] = forms.MultipleChoiceField(
                    choices=[(a.pk, a.text) for a in question.answers.all()],
                    widget=forms.CheckboxSelectMultiple,
                    label=question.text,
                    required=False
                )