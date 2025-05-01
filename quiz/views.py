# from django.views.generic import ListView, DetailView, CreateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.contenttypes.models import ContentType
# from .models import UniversalTest, QuestionType
# # from .forms import TestCreateForm


# class TestListView(ListView):
#     model = UniversalTest
#     template_name = 'quiz/test_list.html'
    
#     def get_queryset(self):
#         queryset = super().get_queryset().filter(is_published=True)
#         if subject_slug := self.kwargs.get('subject_slug'):
#             queryset = queryset.filter(subject__slug=subject_slug)
#         return queryset

# # class TestCreateView(LoginRequiredMixin, CreateView):
# #     model = UniversalTest
# #     form_class = TestCreateForm
# #     template_name = 'quiz/test_create.html'
    
# #     def form_valid(self, form):
# #         form.instance.creator = self.request.user
# #         return super().form_valid(form)

# class TestDetailView(DetailView):
#     model = UniversalTest
#     template_name = 'quiz/test_detail.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['question_types'] = QuestionType.objects.all()
#         return context

# from django.shortcuts import render

# from .models import Test

# def test_detail(request, test_id):
#     test = Test.objects.get(pk=test_id)
#     template = f"quiz/tests/{test.test_type.slug}_detail.html"  # Например: 'tests/exam_detail.html'
#     return render(request, template, {'test': test})

# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Test
# from .serializers import TestSerializer, TestTypeSerializer

# class TestViewSet(viewsets.ModelViewSet):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer

#     @action(detail=False, methods=['get'])
#     def types(self, request):
#         '''Получение всех возможных типов тестов'''
#         types = [
#             {'value': choice[0], 'display': choice[1]} 
#             for choice in Test.TestType.choices
#         ]
#         serializer = TestTypeSerializer(types, many=True)
#         return Response(serializer.data)
    

from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from quiz.models import Test, UserTestResult
from quiz.forms import TestForm
from quiz.utils import evaluate_answers_by_test

User = get_user_model()

@login_required
def test_view(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        form = TestForm(request.POST, questions=test.questions.all())
        if form.is_valid():
            user_questions_data = {question: value for question, value in form.cleaned_data.items() if question.startswith('question_')}
            
            test_result, created = UserTestResult.objects.get_or_create(
                user=request.user,
                test=test,
                defaults={'completed_at': timezone.now()}
            )
            evaluated_result = evaluate_answers_by_test(test, user_questions_data, test_result)
            
            if evaluated_result: test_result.is_passed = False # DEVELOPMENT 
            
            total_score = sum(answer.score for answer in test_result.user_answers.all())
            test_result.score = total_score
            
            if not created:
                test_result.completed_at = timezone.now()
                
            test_result.save()

            messages.info(request, f'Молодец! Работа выполнена, результаты уже доступны, страница их показа в разработке')
            url_redirect = reverse('test-result', args=(test_id, ))
            return redirect(url_redirect)
    else:
        form = TestForm(questions=test.questions.all())
    
    return render(request, 'quiz/test_template.html', {'form': form, 'test': test})

@login_required
def test_result_view(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    user_test = UserTestResult.objects.get(user=request.user, test=test)
    form = TestForm(questions=test.questions.all(), instance=user_test)

    correct_fields = []
    incorrect_fields = []

    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'

    user_answers = user_test.user_answers.all()

    for user_answer in user_answers:
        question_pk = user_answer.question.pk

        if user_answer.is_correct:
            correct_fields.append(f'question_{question_pk}')
        else:
            incorrect_fields.append(f'question_{question_pk}')
        
    context = {
        'form': form, 
        'test': test, 
        'correct_fields': correct_fields, 
        'incorrect_fields': incorrect_fields
    }

    return render(request, 'quiz/test_result_template.html', context=context)


class TestStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Общая статистика
        context['total_tests'] = Test.objects.count()
        context['total_attempts'] = UserTestResult.objects.count()
        context['avg_score'] = UserTestResult.objects.aggregate(
            avg=Avg('score')
        )['avg'] or 0

        # Статистика по тестам
        context['test_stats'] = Test.objects.annotate(
            attempts=Count('user_results'),
            avg_score=Avg('user_results__score')
        ).order_by('-attempts')

        # Статистика по пользователям
        context['user_stats'] = User.objects.annotate(
            tests_completed=Count('test_results'),
            avg_score=Avg('test_results__score')
        ).order_by('-tests_completed')[:10]

        return context
