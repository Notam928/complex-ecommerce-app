from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()



class UserLoginForm(AuthenticationForm):
    
    error_messages = {
        "invalid_login": (
            "Email address or password is incorrect"
        )
    }
    
    username = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Email", }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))   
    rememberme = forms.BooleanField(widget=forms.CheckboxInput(attrs={"id":"save-pass"}), required=False)     
    

class UserSignupForm(UserCreationForm):
    """
    User cration form
    :return html input element
    """
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    
    class Meta:
        model =User
        fields = ("email", )
        error_messages = {
            'email': {
                'unique': "This email is already taken",
                "incomplete":"This email address is invalid"
            }
        }


