from django.db import models


# Create your models here.

class AppUser(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    profile_picture = models.ImageField(upload_to='assets/', null=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - Posted by {self.user}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f'Commented by {self.user} on {self.post}'


class Following(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='followed_by')

    def __str__(self):
        return f'{self.user.id} {self.user.name} follows {self.followed_user.id} {self.followed_user.name}'


class SportEvent(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, default=None, null=True)
    description = models.TextField()
    date = models.DateTimeField()
    category = models.ForeignKey('SportCategory', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.date}'


class SportCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_follower', 'New Follower'),
        ('new_comment', 'New Comment'),
        ('new_post', 'New Post'),
    )

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='receiver')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.notification_type} - {self.sender} to {self.receiver}'
