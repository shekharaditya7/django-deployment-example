from django import forms
from django.core import validators
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo



def check_for_z(value):
    if value[0].lower()!='z':
        raise forms.ValidationError("Names Need to Start with Z")

class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label = "Enter your email again")
    text = forms.CharField(widget=forms.Textarea)


    """
    botcatcher = forms.CharField(required =  False,
                                widget = forms.HiddenInput,
                                validators = [validators.MaxLengthValidator(0)])
    """

    """
    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']
        if len(botcatcher) > 0:
            raise forms.ValidationError("GOTCHA BOT")
        return botcatcher
    """

    def clean(self):
        all_clean_data  = super().clean()
        email = all_clean_data['email']
        verify_email = all_clean_data['verify_email']

        if email != verify_email:
            raise forms.ValidationError("Make sure emails match")



class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta():
            model = User
            fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
