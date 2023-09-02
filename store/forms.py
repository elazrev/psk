from django import forms

# First questionnaire
class TaskOnePart1(forms.Form):
    #first question
    question_1 = "1. ארבעה דברים שאתה עושה כרגע בחייך וצריך להפסיק:"
    input_1_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_4 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    #second question
    question_2 = "2. ארבעה דברים שאתה לא עושה כרגע בחייך וצריך להתחיל לעשות:"
    input_2_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_4 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # third question
    question_3 = "3. שלושה דברים/הרגלים בחייך שאתה לא משלים איתם והגיע הזמן שתשלים איתם:"
    input_3_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_3_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_3_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))


    # fourth question
    question_4 = "4. שלושה דברים/הרגלים רעים בחייך שאתה משלים איתם והגיע הזמן שתפסיק להשלים איתם:"
    input_4_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_4_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_4_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def get_dictionary(self):
        data = {'part_1': {
            self.question_1: [self.cleaned_data['input_1_1'], self.cleaned_data['input_1_2'],
                           self.cleaned_data['input_1_3'], self.cleaned_data['input_1_4']],
            self.question_2: [self.cleaned_data['input_2_1'], self.cleaned_data['input_2_2'],
                           self.cleaned_data['input_2_3'], self.cleaned_data['input_2_4']],
            self.question_3: [self.cleaned_data['input_3_1'], self.cleaned_data['input_3_2'],
                           self.cleaned_data['input_3_3']],
            self.question_4: [self.cleaned_data['input_4_1'], self.cleaned_data['input_4_2'],
                           self.cleaned_data['input_4_3']],
        }}
        return data


class TaskOnePart2(forms.Form):
    # first question
    question_1 = "1. ארבעה דברים שאתה עושה כרגע בחייך וצריך להפסיק:"
    input_1_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_1_4 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # second question
    question_2 = "2. ארבעה דברים שאתה לא עושה כרגע בחייך וצריך להתחיל לעשות:"
    input_2_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_3 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    input_2_4 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def get_dictionary(self):
        data = {'part_02': {
            self.question_1: [self.cleaned_data['input_1_1'], self.cleaned_data['input_1_2'],
                           self.cleaned_data['input_1_3'], self.cleaned_data['input_1_4']],
            self.question_2: [self.cleaned_data['input_2_1'], self.cleaned_data['input_2_2'],
                           self.cleaned_data['input_2_3'], self.cleaned_data['input_2_4']],
        }}
        return data
