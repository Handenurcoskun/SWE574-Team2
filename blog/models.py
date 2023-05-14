from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from spaces.models import Space, SpaceMembership

class Post(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'

    POLICY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]

    policy = models.CharField(max_length=10, choices=POLICY_CHOICES, default=PUBLIC)
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length = 500)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(default='')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    favourites = models.ManyToManyField(User, related_name='favourites', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)                                                                            
    tags = TaggableManager(blank=True)
    image = models.ImageField(default='post_default.jpg', upload_to='post_pics', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-date_posted',)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 200)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'
