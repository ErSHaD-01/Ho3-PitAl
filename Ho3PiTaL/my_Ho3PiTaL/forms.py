from django import forms
from django.contrib.auth.models import User
from . import models

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['age', 'national_code']

    username = forms.CharField(max_length = 150)
    password = forms.CharField(widget = forms.PasswordInput)
    first_name = forms.CharField(max_length = 255)
    last_name = forms.CharField(max_length = 255)



class LoginForm(forms.Form):
    username = forms.CharField(max_length = 150)
    password = forms.CharField(widget = forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            return None
        return password    

class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['doctor' , 'date' , 'text']
      