from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Comment, Recipe


# Create/Register User Form

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Authentication Form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'ingredients', 'instructions', 'preparation_time', 'cooking_time',
                  'servings', 'category', 'difficulty']
        widgets = {
            'author': forms.HiddenInput(),  # Rendi il campo 'author' nascosto nel form
            'user': forms.HiddenInput(),  # Rendi il campo 'user' nascosto nel form
        }
