from django import forms
from django.forms import ModelForm
from .models import userRegistration
from django.contrib.auth.forms import UserCreationForm

class registration_login_form(UserCreationForm):
    class Meta:
        model= userRegistration
        fields= ('username','email','password1','password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) > 20:
            raise forms.ValidationError('Password cannot exceed 20 characters')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        
        return password