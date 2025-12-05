from django import forms
from django.contrib.auth.hashers import make_password
from .models import User


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'signup-password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'signup-password-confirm'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'full_name')
        widgets = {
            'username': forms.TextInput(attrs={'id': 'signup-username'}),
            'full_name': forms.TextInput(attrs={'id': 'signup-fullname'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('The two password fields didn\'t match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)

        user.password = make_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
