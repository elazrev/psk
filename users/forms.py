from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='שם משתמש')
    password1 = forms.CharField(label='סיסמה', widget=forms.PasswordInput)
    password2 = forms.CharField(label='אמת סיסמה', widget=forms.PasswordInput)
    email = forms.EmailField(label='אימייל')
    first_name = forms.CharField(label='שם פרטי')
    last_name = forms.CharField(label='שם משפחה')
    invitee_code = forms.CharField(max_length=8, required=False, label='קוד מנהל')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'invitee_code']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
