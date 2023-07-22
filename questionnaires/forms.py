from django import forms
from .models import Questionnaire, QuestionFile, Question

class QuestionFileForm(forms.ModelForm):
    class Meta:
        model = QuestionFile
        fields = ['file_type', 'title', 'explanation']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class QuestionnaireCreateForm(forms.ModelForm):
    question_files = forms.inlineformset_factory(
        Questionnaire, 
        QuestionFile, 
        form=QuestionFileForm, 
        formset=forms.inlineformset_factory(
            QuestionFile, 
            Question, 
            form=QuestionForm, 
            extra=1,
            min_num=1  # Ensure at least one question is required
        ),
        extra=1
    )

    class Meta:
        model = Questionnaire
        fields = ['title', 'explanation']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        if not self.instance.interviewer:
            self.instance.interviewer = self.user.interviewer
        return super().save(commit)
