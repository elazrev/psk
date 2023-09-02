from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView
from .forms import TaskOnePart1, TaskOnePart2
from django.urls import reverse_lazy


TASK_LIST = ([])
SESSIONS_LIST = ([])


# Store pages
class StoreView(TemplateView):
    template_name = "store/home.html"
    
    
# Static Tasks 

class FirstImpressionView(TemplateView):
    template_name = "static_tasks/01_first_task.html"

class TaskOnePart1View(FormView):
    template_name = 'static_tasks/01_first_task_form.html'
    form_class = TaskOnePart1
    success_url = reverse_lazy('01_form_part_2')

class TaskOnePart2View(FormView):
    template_name = 'static_tasks/02_first_task_form.html'
    form_class = TaskOnePart2
    success_url = reverse_lazy('done')

    

# Static Sessions