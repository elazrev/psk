from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questionnaire
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Questionnaire


class QuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_list.html'
    context_object_name = 'questionnaires'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the query parameter from the URL
        query = self.request.GET.get('q')

        if query:
            # Filter the queryset to match the search query
            queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the search query to the template context
        context['search_query'] = self.request.GET.get('q')

        return context
    
class QuestionnaireCreateView(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title']
    template_name = 'manager/questionnaire_create.html'
    success_url = reverse_lazy('surveys:questionnaire_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    model = Questionnaire
    template_name = 'manager/questionnaire_detail.html'


class QuestionnaireUpdateView(LoginRequiredMixin, UpdateView):
    model = Questionnaire
    fields = ['title']
    template_name = 'manager/questionnaire_update.html'
    success_url = reverse_lazy('surveys:questionnaire_list')
    

class QuestionnaireDeleteView(LoginRequiredMixin, DeleteView):
    model = Questionnaire
    template_name = 'manager/questionnaire_delete.html'
    success_url = reverse_lazy('surveys:questionnaire_list')
