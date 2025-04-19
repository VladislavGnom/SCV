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