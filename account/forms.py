from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-reg',
                                                                 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-reg',
                                                                  'placeholder': 'Repeat password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
            field.help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-reg',
                                               'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-reg',
                                                 'placeholder': 'First name'}),
            'email': forms.TextInput(attrs={'class': 'form-reg',
                                            'placeholder': 'email'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']