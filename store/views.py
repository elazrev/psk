from django.shortcuts import render, redirect
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
    
    
# Static Tasks 

class FirstImpressionView(TemplateView):
    template_name = "static_tasks/01_first_task.html"

# Static forms
class TaskOnePart1View(FormView):
    template_name = 'static_tasks/01_first_task_form.html'
    form_class = TaskOnePart1
    success_url = reverse_lazy('01_form_part_2')

    def form_valid(self, form):
        if form.is_valid():
            data = form.get_dictionary()
            full_answer = FullAnswer(
                sender=self.request.user,
                responder=self.request.user,
                questionnaire="Task 1 Part 1",
                content=form.get_dictionary(),
            )
            full_answer.save()
            return super().form_valid(form)
        else:
            print("form isn't valid")
            return self.form_invalid(form)


class TaskOnePart2View(FormView):
    template_name = 'static_tasks/02_first_task_form.html'
    form_class = TaskOnePart2
    success_url = reverse_lazy('done')

    def form_valid(self, form):
        if form.is_valid():
            full_answer = FullAnswer.objects.get(
                sender=self.request.user,
                responder=self.request.user,
                questionnaire="Task 1 Part 1",
            )

            full_answer.content.update(form.get_dictionary())

            full_answer.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
