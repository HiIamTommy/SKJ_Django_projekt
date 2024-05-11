from django import forms
from .models import AppUser, Comment, Post


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
