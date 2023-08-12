from django import forms
from surveys.models import Obj, Answer


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
        model = Obj, Answer
        fields = ['content']