from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import transaction
from .models import UserProfile

class SignupForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username','email','password1','password2')
    @transaction.atomic
    def save(self):
        user = super().save()
        return user
   