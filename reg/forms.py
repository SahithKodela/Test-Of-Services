from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

#User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("Username or password is wrong")

        return super(LoginForm,self).clean(*args,**kwargs)

class Reg(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_enter_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=[
            'username',
            'password',
            're_enter_password',
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        re_enter_password = self.cleaned_data.get('re_enter_password')
        if password != re_enter_password:
            raise forms.ValidationError("Password is not matching")