from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    def __init__(self,*args,**kwargs):
        self.helper = FormHelper()
        self.helper.help_text_inline = True
        super().__init__(*args,**kwargs)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("There is a user using this email. Use another email or sign in instead")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']