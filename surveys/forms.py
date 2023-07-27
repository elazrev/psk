from django import forms
from .models import Questionnaire, QuestionSet, Question
from django.utils import timezone

class QuestionnaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['creator'].initial = user
            self.fields['owner'].initial = user
            

    class Meta:
        model = Questionnaire
        fields = ['title', 'survey_type']

class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ['title', 'explanation', 'hints', 'set_type', 'hierarchy_location']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_set', 'question_text', 'hierarchy_location']

class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'hierarchy_location']

class DeleteQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = []  # לא נצטרך להציג כל שדות, זו פורם למחיקה בלבד
