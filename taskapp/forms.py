from django import forms
from django.contrib.auth.forms import UserCreationForm

from taskapp.models import User, Task, TaskCompletionReport  

class SigninForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2','email','user_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            
        }
class loginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'admin', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'admin': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
class TaskCompletionReportForm(forms.ModelForm):
    class Meta:
        model = TaskCompletionReport
        fields = ['worked_hours', 'completion_report']
        widgets = {
            'worked_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'completion_report': forms.Textarea(attrs={'class': 'form-control'}),
        }