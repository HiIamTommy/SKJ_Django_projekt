from django import forms
from .models import AppUser, Comment, Post, SportEvent, SportCategory


class LoginForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'surname', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3})
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'surname', 'email', 'password']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']


class AddSportEventForm(forms.ModelForm):
    class Meta:
        model = SportEvent
        fields = ['title', 'description', 'date', 'category']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class AddSportCategoryForm(forms.ModelForm):
    class Meta:
        model = SportCategory
        fields = ['name']


class UpdateSportEventForm(forms.ModelForm):
    class Meta:
        model = SportEvent
        fields = ['title', 'description', 'date', 'category']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

