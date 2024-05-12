import tempfile
from PIL import Image
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponseRedirect
import requests
import random

from django.urls import reverse

from .forms import LoginForm, RegisterForm, CommentForm, UpdateUserForm, AddPostForm, AddSportEventForm, \
    AddSportCategoryForm
from .models import AppUser, Post, Comment, Following, Notification, SportEvent


# Create your views here.
def index(request):
    users = AppUser.objects.all()
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, "stations/index.html",
                  {"users": users, "login_form": login_form, "register_form": register_form})


def login(request, user_id=None):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = AppUser.objects.filter(email=email, password=password).first()
            if user is not None:
                following_users = Following.objects.filter(user=user).values_list('followed_user', flat=True)
                posts = Post.objects.filter(user__in=list(following_users) + [user.id])
                not_following_users = AppUser.objects.exclude(id=user.id).exclude(id__in=following_users)[:5]
                return render(request, 'stations/login.html', {
                    'user': user,
                    'posts': posts,
                    'following_users': following_users,
                    'not_following_users': not_following_users,
                })
            else:
                register_form = RegisterForm()
                return render(request, 'stations/index.html', {
                    'register_form': register_form,
                    'login_form': login_form,
                    'error': 'Invalid email or password'
                })
    else:
        login_form = LoginForm()
        if user_id is not None:
            user = AppUser.objects.get(id=user_id)
            following_users = Following.objects.filter(user=user).values_list('followed_user', flat=True)
            posts = Post.objects.filter(user__in=list(following_users) + [user.id])
            not_following_users = AppUser.objects.exclude(id=user.id).exclude(id__in=following_users)[:5]
            return render(request, 'stations/login.html', {
                'user': user,
                'posts': posts,
                'following_users': following_users,
                'not_following_users': not_following_users,
            })
        else:
            return render(request, 'stations/login.html', {'login_form': login_form})


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.name = register_form.cleaned_data['name']
            user.surname = register_form.cleaned_data['surname']
            user.email = register_form.cleaned_data['email']
            user.username = register_form.cleaned_data['username']
            user.password = register_form.cleaned_data['password']

            # Fetch random character image from Rick and Morty API
            response = requests.get('https://rickandmortyapi.com/api/character/')
            total_characters = response.json()['info']['count']

            random_id = random.randint(1, total_characters)

            response = requests.get(f'https://rickandmortyapi.com/api/character/{random_id}')
            character = response.json()

            image_url = character['image']

            response = requests.get(image_url)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()

            img = Image.open(img_temp)

            if img.mode == 'P':
                img = img.convert('RGB')

            img_io = tempfile.TemporaryFile()
            img.save(img_io, format='JPEG')

            user.profile_picture.save(f'{user.username}.jpg', File(img_io))
            #

            user.save()
            messages.success(request, 'Registration successful. Now you can login')
            return redirect('index')
        else:
            messages.error(request, 'Error registering user, please try again')
            return render(request, 'stations/index.html', {'register_form': register_form})
    else:
        register_form = RegisterForm()
        return render(request, 'stations/index.html', {'register_form': register_form})


def add_comment(request, post_id, user_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = AppUser.objects.get(id=user_id)
            comment.post = Post.objects.get(id=post_id)
            comment.body = comment_form.cleaned_data['body']
            comment.save()
            if comment.post.user != comment.user:
                send_notification('new_comment', comment.user, comment.post.user, post=comment.post, comment=comment)
            messages.success(request, 'Comment added successfully')
        else:
            messages.error(request, 'Error adding comment')
    return redirect('login_with_id', user_id=user_id)


def settings(request, user_id):
    print(user_id)
    user = get_object_or_404(AppUser, id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('login_with_id', user_id=user.id)
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'stations/settings.html', {'form': form, 'user': user})


def add_post(request, user_id):
    user = AppUser.objects.get(id=user_id)
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.title = post_form.cleaned_data['title']
            post.body = post_form.cleaned_data['body']
            post.save()
            followers = Following.objects.filter(followed_user=user)
            for f in followers:
                send_notification('new_post', user, f.user, post=post)
            messages.success(request, 'Post added successfully')
            return redirect('login_with_id', user_id=user_id)
    else:
        post_form = AddPostForm()
    return render(request, 'stations/add_post.html', {'post_form': post_form, 'user': user})


def delete_user(request, user_id):
    user = AppUser.objects.get(id=user_id)
    user.delete()
    # return redirect('index', {'user': user})
    return HttpResponseRedirect(reverse('index'))


def notifications(request, user_id):
    user = AppUser.objects.get(id=user_id)
    user_notifications = Notification.objects.filter(receiver=user)
    return render(request, 'stations/notifications.html', {'notifications': user_notifications, 'user': user})


def send_notification(notification_type, sender, receiver, post=None, comment=None):
    notification = Notification(
        notification_type=notification_type,
        sender=sender,
        receiver=receiver,
        post=post,
        comment=comment
    )
    notification.save()


def follow_user(request, user_id, followed_user_id):
    user = AppUser.objects.get(id=user_id)
    follow_user = AppUser.objects.get(id=followed_user_id)
    Following.objects.create(user=user, followed_user=follow_user)
    send_notification('new_follower', user, follow_user)
    return HttpResponseRedirect(reverse('login_with_id', args=[user_id]))


def delete_all_notifications(request, user_id):
    user = AppUser.objects.get(id=user_id)
    notifications = Notification.objects.filter(receiver=user)
    notifications.delete()
    return HttpResponseRedirect(reverse('notifications', args=[user_id]))


def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return HttpResponseRedirect(reverse('notifications', args=[notification.receiver.id]))


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse('login_with_id', args=[comment.user.id]))


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('login_with_id', args=[post.user.id]))


def follower_list(request, user_id):
    user = AppUser.objects.get(id=user_id)
    following_users = Following.objects.filter(user=user)
    return render(request, 'stations/follower_list.html', {'following_users': following_users, 'user': user})


def unfollow_user(request, user_id, followed_user_id):
    user = AppUser.objects.get(id=user_id)
    following = Following.objects.get(user__id=user_id, followed_user__id=followed_user_id)
    following.delete()
    return HttpResponseRedirect(reverse('follower_list', args=[user.id]))


def user_detail(request, user_id, detailed_id):
    user = AppUser.objects.get(id=user_id)
    detailed_user = AppUser.objects.get(id=detailed_id)
    posts = Post.objects.filter(user=detailed_user)
    return render(request, 'stations/user_detail.html', {'detailed_user': detailed_user, 'posts': posts, 'user': user})


def sport_events(request, user_id):
    user = AppUser.objects.get(id=user_id)
    events = SportEvent.objects.all()
    return render(request, 'stations/sport_events.html', {'events': events, 'user': user})


def add_sport_event(request, user_id):
    user = AppUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = AddSportEventForm(request.POST)
        if form.is_valid():
            sport_event = form.save(commit=False)
            sport_event.user = user
            sport_event.save()
            return redirect('sport_events', user_id=user_id)
    else:
        form = AddSportEventForm()
    return render(request, 'stations/add_sport_event.html', {'form': form, 'user': user})


def delete_sport_event(request, user_id, event_id):
    user = AppUser.objects.get(id=user_id)
    event = SportEvent.objects.get(id=event_id)
    if user == event.user:
        event.delete()
    return redirect('sport_events', user_id=user_id)


def add_sport_category(request, user_id):
    user = AppUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = AddSportCategoryForm(request.POST)
        if form.is_valid():
            sport_category = form.save(commit=False)
            sport_category.save()
            return redirect('sport_events', user_id=user_id)
    else:
        form = AddSportCategoryForm()  # Use AddSportCategoryForm here
    return render(request, 'stations/add_sport_category.html', {'form': form, 'user': user})


def user_events(request, detailed_id, user_id):
    logged_user = AppUser.objects.get(id=user_id)
    detailed_user = AppUser.objects.get(id=detailed_id)
    events = SportEvent.objects.filter(user=detailed_user)
    return render(request, 'stations/user_events.html', {'events': events, 'logged_user': logged_user, 'detailed_user': detailed_user})
