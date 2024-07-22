from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from captcha.fields import CaptchaField

from shop.models import Products, ProductOffers


input_attrs = {"class": "form-input"}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(input_attrs))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(input_attrs))


class RegisterUserForm(UserCreationForm):
    date_birth = forms.CharField(label="Date of birth",
                                 widget=forms.DateInput(format='%d-%m-%Y',
                                                        attrs={'type': 'date'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(input_attrs))
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(input_attrs))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(input_attrs))
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput(input_attrs))
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = ('username', "email", 'password1',
                  'password2', "gender_choice", "image",
                  'captcha')


class EditUserForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('description', 'image', 'date_birth', 'gender_choice')


class EditProductForm(ModelForm):

    class Meta:
        model = Products
        fields = ('name', 'categories', 'description')


class EditOfferForm(ModelForm):

    class Meta:
        model = ProductOffers
        fields = ('price', 'is_active')
