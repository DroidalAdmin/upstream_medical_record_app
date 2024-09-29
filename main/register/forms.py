from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterEmailForm(forms.Form):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

class OTPLoginForm(forms.Form):
    otp_1 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    otp_2 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    otp_3 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    otp_4 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    otp_5 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    otp_6 = forms.CharField(label='', max_length=1, widget=forms.TextInput(attrs={'class': 'form-control otp-field', 'maxlength': '1', 'size': '1'}))
    
    def clean(self):
        cleaned_data = super().clean()
        otp = ''.join([cleaned_data.get(f'otp_{i}', '') for i in range(1, 7)])
        cleaned_data['otp'] = otp
        return cleaned_data