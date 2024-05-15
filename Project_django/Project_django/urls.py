"""
URL configuration for Project_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),  # login without user_id
    path('login/<int:user_id>/', views.login, name='login_with_id'),  # login with user_id
    path('register', views.register, name='register'),
    path('add_comment/<int:post_id>/<int:user_id>', views.add_comment, name='add_comment'),
    path('settings/<int:user_id>', views.settings, name='settings'),
    path('add_post/<int:user_id>', views.add_post, name='add_post'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('notifications/<int:user_id>', views.notifications, name='notifications'),
    path('follow_user/<int:user_id>/<int:followed_user_id>', views.follow_user, name='follow_user'),
    path('delete_all_notifications/<int:user_id>', views.delete_all_notifications, name='delete_all_notifications'),
    path('delete_notification/<int:notification_id>', views.delete_notification, name='delete_notification'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('follower_list/<int:user_id>', views.follower_list, name='follower_list'),
    path('unfollow_user/<int:user_id>/<int:followed_user_id>', views.unfollow_user, name='unfollow_user'),
    path('user_detail/<int:user_id>/<int:detailed_id>', views.user_detail, name='user_detail'),
    path('sport_events/<int:user_id>', views.sport_events, name='sport_events'),
    path('add_sport_event/<int:user_id>', views.add_sport_event, name='add_sport_event'),
    path('delete_sport_event/<int:user_id>/<int:event_id>', views.delete_sport_event, name='delete_sport_event'),
    path('add_sport_category/<int:user_id>', views.add_sport_category, name='add_sport_category'),
    path('user_events/<int:detailed_id>/<int:user_id>', views.user_events, name='user_events'),
    path('update_sport_event/<int:user_id>/<int:event_id>', views.update_sport_event, name='update_sport_event'),
    path('search_users', views.search_users, name='search_users'),
]
