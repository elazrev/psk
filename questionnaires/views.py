from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Interviewer, Questionnaire
from .forms import QuestionnaireCreateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class InterviewerListView(ListView):
    model = Interviewer
    template_name = 'questionnaires/interviewer_list.html'
    context_object_name = 'interviewers'


class InterviewerDetailView(DetailView):
    model = Interviewer
    template_name = 'questionnaires/interviewer_detail.html'
    context_object_name = 'interviewer'


class QuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_list.html'
    context_object_name = 'questionnaires'


class QuestionnaireDetailView(DetailView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_detail.html'
    context_object_name = 'questionnaire'


@method_decorator(login_required, name='dispatch')
class QuestionnaireCreateView(CreateView):
    model = Questionnaire
    form_class = QuestionnaireCreateForm
    template_name = 'questionnaires/questionnaire_create.html'
    success_url = reverse_lazy('questionnaires:questionnaire-create-success')

    def form_valid(self, form):
        form.instance.interviewer = self.request.user.interviewer
        return super().form_valid(form)

def create_questionnaire_success(request):
    return render(request, 'questionnaires/questionnaire_create_success.html')
