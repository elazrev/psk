from django.contrib import admin
from .models import Questionnaire, QuestionSet, Question, Answer

admin.site.register(Questionnaire)
admin.site.register(QuestionSet)
admin.site.register(Question)
admin.site.register(Answer)
