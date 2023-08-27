from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView

TASK_LIST = ([])
SESSIONS_LIST = ([])


# Store pages
class StoreView(TemplateView):
    template_name = "store/home.html"
    
    
# Static Tasks 

class FirstImpressionView(TemplateView):
    template_name = "static_tasks/01_first_task.html"
    

# Static Sessions