from functools import partial
from itertools import groupby
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Questionnaire
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Questionnaire, Obj, Answer
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import HiddenInput
from .forms import ObjForm, AnswerForm
from django.views.generic.edit import FormView




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
    fields = ['title', 'description']
    template_name = 'surveys/questionnaire_create.html'
    success_url = reverse_lazy('surveys:questionnaire_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_detail.html'


class QuestionnaireUpdateView(LoginRequiredMixin, UpdateView):
    model = Questionnaire
    fields = ['title', 'description']
    template_name = 'surveys/questionnaire_update.html'
    success_url = reverse_lazy('surveys:questionnaire_list')
    

class QuestionnaireDeleteView(LoginRequiredMixin, DeleteView):
    model = Questionnaire
    template_name = 'surveys/questionnaire_delete.html'
    success_url = reverse_lazy('surveys:questionnaire_list')

# Object section

class ObjListView(ListView):
    model = Obj
    template_name = 'surveys/objects_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        questionnaire_id = self.kwargs['questionnaire_id']
        return Obj.objects.filter(questionnaire_id=questionnaire_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire_id = self.kwargs['questionnaire_id']
        context['questionnaire_id'] = self.kwargs.get('questionnaire_id')
        return context

class ObjDeleteView(LoginRequiredMixin, DeleteView):
    model = Obj
    context_object_name = 'obj'
    success_url = reverse_lazy('surveys:obj_list')
    template_name = 'surveys\question_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': self.object.questionnaire.id})


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Obj
    template_name = 'surveys/question_form.html'

    def get_form_class(self):
        return ObjForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaire_id'] = self.kwargs.get('questionnaire_id')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        questionnaire_id = self.kwargs.get('questionnaire_id')
        if questionnaire_id:
            kwargs['questionnaire_id'] = questionnaire_id
        return kwargs

    def form_valid(self, form):
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        parent = Obj.objects.filter(questionnaire=questionnaire, obj_type='title').last()
        if parent:
            obj = form.save(commit=False)
            obj.parent = parent
            obj.questionnaire = questionnaire
            obj.save()
        else:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        if 'done' in self.request.POST:
            return reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': self.object.questionnaire.id})
        elif 'more' in self.request.POST:
            return reverse_lazy('surveys:new_question', kwargs={'questionnaire_id': self.object.questionnaire.id})

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Obj
    template_name = 'surveys/question_form.html'
    fields = ['obj_type', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaire_id'] = self.kwargs.get('questionnaire_id')
        return context
    
    def get_success_url(self):
        return reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': self.object.questionnaire.id})

# spacial options => Divider, Title, Explanaition, Hints 
class DividerCreateView(LoginRequiredMixin, CreateView):
    model = Obj
    fields = []
    template_name = 'surveys/divider_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        last_title = Obj.objects.filter(questionnaire=questionnaire, obj_type='title').last()
        context['last_title'] = last_title
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        obj.questionnaire = questionnaire
        obj.obj_type = 'divider'
        obj.content = '.'
        parent = Obj.objects.filter(questionnaire=questionnaire, obj_type='title').last()
        if parent:
            obj.parent = parent
        else:
            obj.parent = None
        obj.save()
        return redirect(reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': questionnaire_id}))
    
class TitleCreateView(LoginRequiredMixin, CreateView):
    model = Obj
    context_object_name = 'obj'
    fields = ['content']
    template_name = 'surveys/title_form.html'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        obj.questionnaire = questionnaire
        obj.obj_type = 'title'
        obj.parent = None
        obj.save()
        return redirect(reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': questionnaire_id}))
    
    
class ExplanationCreateView(LoginRequiredMixin, CreateView):
    model = Obj
    context_object_name = 'obj'
    fields = ['content']
    template_name = 'surveys/explanation_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        obj.questionnaire = questionnaire
        obj.obj_type = 'explanation'
        parent = Obj.objects.filter(questionnaire=questionnaire, obj_type='title').last()
        if parent:
            obj.parent = parent
        else:
            obj.parent = None
        obj.save()
        return redirect(reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': questionnaire_id}))
    
    

class HintCreateView(LoginRequiredMixin, CreateView):
    model = Obj
    context_object_name = 'obj'
    fields = ['content']
    template_name = 'surveys/hint_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        obj.questionnaire = questionnaire
        obj.obj_type = 'hints'
        parent = Obj.objects.filter(questionnaire=questionnaire, obj_type='title').last()
        if parent:
            obj.parent = parent
        else:
            obj.parent = None
        obj.save()
        return redirect(reverse_lazy('surveys:obj_list', kwargs={'questionnaire_id': questionnaire_id}))
    
    
    # Answer section
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from .forms import DynamicQuestionnaireForm
from .models import Questionnaire, Obj

class AnswerCreateView(LoginRequiredMixin, FormView):
    template_name = 'surveys/answer_form.html'
    form_class = DynamicQuestionnaireForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        questionnaire_id = self.kwargs.get('questionnaire_id')
        objects = Obj.objects.filter(questionnaire_id=questionnaire_id)
        kwargs['objects'] = objects
    
        initial_data = {}
        for question in objects:
            obj_type = question.obj_type
            field_name = f"{obj_type}"
            if obj_type == 'open_question' or obj_type == 'Completing':
                initial_data[field_name] = ''  # Set initial value for open_question and Completing

        kwargs['initial'] = initial_data

        return kwargs

    
    def form_valid(self, form):
        questionnaire_id = self.kwargs['questionnaire_id']
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        questions = Obj.objects.filter(questionnaire=questionnaire).all()

        for question in questions:
            answer_content = form.cleaned_data[f"answer_{question.id}"]
            Answer.objects.create(
                sender=self.request.user,  # Set the sender field to the logged-in user
                responder=self.request.user,
                question=question,
                content=answer_content
            )

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire_id = self.kwargs.get('questionnaire_id')
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        objects = Obj.objects.filter(questionnaire=questionnaire).all()
        context['questionnaire'] = questionnaire
        context['objects'] = objects

        form = self.get_form()  # Get the form instance
        context['form'] = form  # Add the form instance to the context

        return context

    
# New structure of handlings

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import FullTask, FullAnswer
from .forms import FullTaskForm, FullAnswerForm

class FullTaskListView(ListView):
    model = FullTask
    template_name = 'tasks/task_list.html'
    context_object_name = 'fulltasks'  # The variable name to use in the template
    
class FullTaskDetailView(DetailView):
    model = FullTask
    template_name = 'tasks/task_detail.html'  # Update with your template path
    context_object_name = 'fulltask'

class FullTaskCreateView(CreateView):
    model = FullTask
    form_class = FullTaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')  # Define a URL to redirect to upon successful form submission

class FullTaskUpdateView(UpdateView):
    model = FullTask
    form_class = FullTaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')  # Define a URL to redirect to upon successful form submission

class FullAnswerCreateView(CreateView):
    model = FullAnswer
    form_class = FullAnswerForm
    template_name = 'fullanswer_create.html'
    success_url = reverse_lazy('fullanswer_list')  # Define a URL to redirect to upon successful form submission

class FullAnswerUpdateView(UpdateView):
    model = FullAnswer
    form_class = FullAnswerForm
    template_name = 'fullanswer_update.html'
    success_url = reverse_lazy('fullanswer_list')  # Define a URL to redirect to upon successful form submission

