from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Questionnaire, QuestionSet, Question
from .forms import QuestionnaireForm, QuestionSetForm, QuestionForm, EditQuestionForm, DeleteQuestionForm
from django.views.generic.edit import FormMixin


# Create a list of all questionnaires
class QuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_list.html'
    context_object_name = 'questionnaires'


class QuestionnaireDetailView(DetailView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = self.object
        question_sets = QuestionSet.objects.filter(questionnaire=questionnaire)
        questions = Question.objects.filter(question_set__in=question_sets)
        context['question_sets'] = question_sets
        context['questions'] = questions
        return context

    
    
class QuestionnaireCreateView(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title', 'survey_type']
    template_name = 'surveys/questionnaire_create.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Get the pk of the newly created questionnaire
        questionnaire_pk = self.object.pk
        # Redirect to the detail view of the newly created questionnaire
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})
    

class QuestionnaireUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Questionnaire
    fields = ['title', 'survey_type']
    template_name = 'surveys/questionnaire_form.html'
   
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator
    
    def get_success_url(self):
        # Get the pk of the newly created questionnaire
        questionnaire_pk = self.object.pk
        # Redirect to the detail view of the newly created questionnaire
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})
    

class QuestionnaireDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_confirm_delete.html'
    success_url = '/manager/surveys/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator



class QuestionSetCreateView(CreateView, FormMixin):
    model = QuestionSet
    fields = ['title','explanation', 'hints', 'set_type']
    template_name = 'surveys/questionset_create.html'
    
    def form_valid(self, form):
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_pk)
        form.instance.questionnaire = questionnaire
        form.instance.hierarchy_counter()
        return super().form_valid(form)
    
    def get_success_url(self):
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})


class QuestionSetUpdateView(UpdateView):
    model = QuestionSet
    fields = ['title','explanation', 'hints', 'set_type']
    template_name = 'surveys/questionset_form.html'
    
    def form_valid(self, form):
        # Get the associated questionnaire
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_pk)
        form.instance.questionnaire = questionnaire
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the questionnaire detail view
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})

class QuestionSetDeleteView(DeleteView):
    model = QuestionSet
    template_name = 'surveys/question_set_confirm_delete.html'
    context_object_name = 'questionset'
    success_url = reverse_lazy('surveys:questionnaire_list')


# Question section
from django.urls import reverse_lazy

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'surveys/question_form.html'
    
    def form_valid(self, form):
        # Get the associated question_set
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        question_set = get_object_or_404(QuestionSet, questionnaire__pk=questionnaire_pk, pk=self.kwargs['question_set_pk'])
        form.instance.question_set = question_set
        form.instance.hierarchy_counter()
        return super().form_valid(form)
    
    def get_success_url(self):
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})


from django.http import Http404

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'surveys/question_form.html'

    def get_object(self, queryset=None):
        try:
            # Get the associated question_set and retrieve the correct question
            questionnaire_pk = self.kwargs.get('questionnaire_pk')
            question_set_pk = self.kwargs.get('question_set_pk')
            question_pk = self.kwargs.get('pk')
            return Question.objects.get(
                question_set__questionnaire__pk=questionnaire_pk,
                question_set__pk=question_set_pk,
                pk=question_pk
            )
        except Question.DoesNotExist:
            raise Http404("Question does not exist.")

    def get_success_url(self):
        questionnaire_pk = self.kwargs.get('questionnaire_pk')
        question_set_pk = self.kwargs.get('question_set_pk')
        return reverse('surveys:questionnaire_detail', kwargs={'pk': questionnaire_pk})

    
class QuestionDeleteView(DeleteView):
    model = Question
    form_class = DeleteQuestionForm
    template_name = 'surveys/question_confirm_delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('surveys:questionnaire_list')
