from django import forms
from django.contrib.auth import authenticate, get_user_model
from main.models import *


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['login']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid user or password")
        self.user = user
        return cleaned_data


class UserForm(forms.Form):

    login = forms.CharField()
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput, strip=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    club = forms.ModelChoiceField(queryset=Clubs.objects.all(),
                                   required=True)

    def clean_login(self):
        from django.contrib.auth.models import User
        login = self.cleaned_data.get("login")
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError("A user with that login already exists.")
        return login

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2


class ResetPasswordForm(forms.Form):

    new_password1 = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Repeat new password", widget=forms.PasswordInput, strip=False)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2


class ClubListForm(forms.Form):
    phrase = forms.ModelChoiceField(queryset=Leagues.objects.all(), required=True, label='Search clubs in:')


class PlayerSearchForm(forms.Form):
    phrase = forms.CharField(label="Player search")


class ClubSearchForm(forms.Form):
    phrase = forms.CharField(label="Club search")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_sent', 'sender']