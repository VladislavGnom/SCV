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
    

from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from quiz.models import Test


class TestHandleView(View):
    def get(self, request, pk):
        self.test_obj = get_object_or_404(Test, pk=pk)

        context = self.get_context_data()
        return render(request, 'quiz/main_test_page.html', context=context)
    
    def get_context_data(self, **kwargs):
        context = {}
        context['test'] = self.test_obj
        return context