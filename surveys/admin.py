from django.contrib import admin
from .models import Questionnaire, Obj, Answer, FullAnswer

admin.site.register(Questionnaire)
admin.site.register(Obj)
admin.site.register(Answer)
admin.site.register(FullAnswer)
