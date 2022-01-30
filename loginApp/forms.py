from django import forms
from .models import User
from .models import SeasonCode
from loginApp.password_validator import password_custome_validate as validator


class login_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
    
class forgot_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
        
        
        
class register_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','password')        
        