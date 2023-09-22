from django import forms
from django.shortcuts import get_object_or_404
from surveys.models import Obj, Answer, Questionnaire
from django.forms import formset_factory


class ObjForm(forms.ModelForm):
    class Meta:
        model = Obj
        fields = ['obj_type', 'content']

    def __init__(self, questionnaire_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if questionnaire_id:
            title_qs = Obj.objects.filter(questionnaire__id=questionnaire_id, obj_type='title')
            if title_qs.exists():
                self.parent = title_qs.last()
            question_choices = [
                ('open_question', 'שאלה פתוחה'),
                ('single_choice', 'שאלת בחירה בודדת'),
                ('multiple_choice', 'שאלת בחירה מרובה'),
                ('rating', 'שאלת דירוג'),
                ('agreement', 'שאלת הצבה'),
                ('self_rating', 'שאלת דירוג עצמי'),
                ('self_choice', 'שאלת בחירה עצמית'),
                ('Completing', 'השלמת משפטים'),
            ]
            self.fields['obj_type'].choices = question_choices
            self.fields['obj_type'].widget.attrs.update({'class': 'form-control'})
            
            

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Obj
        fields = ['content']
        
        
class BaseAnswerFormSet(forms.BaseModelFormSet):
    def __init__(self, questionnaire, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Obj.objects.filter(questionnaire=questionnaire).all()
 
 
        
from django import forms
from surveys.models import Obj

class DynamicQuestionnaireForm(forms.Form):
    def __init__(self, *args, objects=None, **kwargs):
        super().__init__(*args, **kwargs)
        if objects:
            for question in objects:
                obj_type = question.obj_type
                field_name = f"answer_{question.id}_{obj_type}"
                
                if obj_type == 'title':
                    self.fields[field_name] = forms.CharField(
                        label=question.content,
                        widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                        required=False
                    )
                elif obj_type == 'explanation':
                    self.fields[field_name] = forms.CharField(
                        label=question.content,
                        widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                        required=False
                    )
                elif obj_type == 'image':
                    self.fields[field_name] = forms.ImageField(
                        label=question.content,
                        required=False
                    )
                elif obj_type == 'divider':
                    self.fields[field_name] = forms.CharField(
                        widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                        required=False
                    )
                elif obj_type == 'hints':
                    self.fields[field_name] = forms.CharField(
                        label=question.content,
                        widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                        required=False
                    )
                elif obj_type == 'open_question':
                    self.fields[field_name] = forms.CharField(
                        label=question.content,
                        widget=forms.Textarea(attrs={'rows': 1}),
                        required=False
                    )
                elif obj_type == 'single_choice':
                    choices = question.text_spliter()
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.content,
                        widget=forms.RadioSelect,
                        choices=[(choice, choice) for choice in choices],
                        initial='',  # Set initial value as an empty string
                        required=False
                    )
                elif obj_type == 'multiple_choice':
                    choices = question.text_spliter()
                    self.fields[field_name] = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        choices=[(choice, choice) for choice in choices],
                        required=False
                        )
                elif obj_type == 'rating':
                    choices = [(str(i), str(i)) for i in range(1, 6)]
                    field_label = question.content
    
                    self.fields[field_name] = forms.ChoiceField(
                        widget=forms.RadioSelect(attrs={'class': 'small form-check-lable'}),
                        choices=choices,
                        label=field_label,
                        required=False
                    )

                elif obj_type == 'Completing':
                    self.fields[field_name] = forms.CharField(
                        label=question.content.replace(';', '_____'),
                        widget=forms.Textarea(attrs={'rows': 1}),
                        required=False
                    )
                self.initial[field_name] = ''  # Set initial value for this field if needed

                # print(f"Added field: {field_name}, type: {type(self.fields[field_name])}") #Debugging 
        

from .models import FullTask, FullAnswer, CATEGORY_CHOICES, SUB_CATEGORY_CHOICES

OBJ_TYPE_CHOICES = (
        ('title', 'כותרת'),
        ('explanation', 'הסבר'),
        ('image', 'תמונה'),
        ('hints', 'רמזים'),
        ('open_question', 'שאלה פתוחה'),
        ('single_choice', 'שאלת בחירה בודדת'),
        ('multiple_choice', 'שאלת בחירה מרובה'),
        ('rating', 'שאלת דירוג'),
        ('agreement', 'שאלת הצבה'),
        ('self_rating', 'שאלת דירוג עצמי'),
        ('self_choice', 'שאלת בחירה עצמית'),
        ('Completing', 'השלמת משפטים'),
    )

class ContentForm(forms.Form):
    obj_type = forms.ChoiceField(choices=OBJ_TYPE_CHOICES)
    obj_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    answer_field = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    hints = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    related_with = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    
 
class FullTaskForm(forms.ModelForm):
    content = forms.JSONField(widget=forms.HiddenInput(), required=False)
    category = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    sub_category = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = FullTask
        fields = ['title', 'creator', 'category', 'sub_category', 'sub_title', 'category']

    def __init__(self, *args, **kwargs):
        super(FullTaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = CATEGORY_CHOICES
        self.fields['sub_category'].choices = SUB_CATEGORY_CHOICES

        # Set initial value for content if editing an existing task
        if self.instance.pk:
            self.initial['content'] = self.instance.content

    def clean_content(self):
        content_data = self.cleaned_data.get('content')
        content_form = ContentForm(content_data)

        if not content_form.is_valid():
            raise forms.ValidationError('Invalid content data')

        return content_form.cleaned_data


class FullAnswerForm(forms.ModelForm):
    class Meta:
        model = FullAnswer
        fields = ['sender', 'responder', 'questionnaire', 'answered_task', 'content', 'date_sent', 'date_responed']
