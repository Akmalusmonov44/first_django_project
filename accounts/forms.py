from django import forms
from django.forms import PasswordInput
from django.contrib.auth.models import User
from .models import Profile
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Parol', widget=PasswordInput)
    password_2 = forms.CharField(label='Parolni qayta kiriting', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password_2'):
            raise forms.ValidationError('Parollar mos kelmadi.')
        return data['password_2']
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']