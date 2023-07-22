from django.contrib import admin
from .models import Interviewer, Interviewed, Questionnaire, QuestionFile, Question

# Register your models here
admin.site.register(Interviewer)
admin.site.register(Interviewed)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionFileInline(admin.TabularInline):
    model = QuestionFile
    extra = 1

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionFileInline]

@admin.register(QuestionFile)
class QuestionFileAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
