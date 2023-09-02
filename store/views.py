from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView
from .forms import TaskOnePart1, TaskOnePart2
from django.urls import reverse_lazy
from surveys.models import FullAnswer


TASK_LIST = ([])
SESSIONS_LIST = ([])


# Store pages
class StoreView(TemplateView):
    template_name = "store/home.html"

class DoneView(TemplateView):
    template_name = "store/done.html"
    
# Static Tasks 

class FirstImpressionView(TemplateView):
    template_name = "static_tasks/01_first_task.html"


# Static forms
class TaskOnePart1View(FormView):
    template_name = 'static_tasks/01_first_task_form.html'
    form_class = TaskOnePart1
    success_url = reverse_lazy('store:01_form_part_2')

    def form_valid(self, form):
        print("valid!")
        data = form.get_dictionary()
        # Create a FullAnswer instance and save it
        FullAnswer.objects.create(
            sender=self.request.user,
            responder=self.request.user,  # You can change this to the actual responder
            questionnaire="Task One",  # You can change this to the actual questionnaire name
            content=data,
        )
        return super().form_valid(form)

class TaskOnePart2View(FormView):
    template_name = 'static_tasks/02_first_task_form.html'
    form_class = TaskOnePart2
    success_url = reverse_lazy('store:done')
    
    def form_valid(self, form):
        data = form.get_dictionary()
        
        # Get the existing FullAnswer object if it exists
        full_answer = get_object_or_404(
            FullAnswer,
            sender=self.request.user,
            responder=self.request.user,
            questionnaire="Task One"  # Make sure to match the correct questionnaire name
        )
        
        # Update the content
        full_answer.content.update(data)
        full_answer.save()
        
        return super().form_valid(form)
    

# Static Sessions