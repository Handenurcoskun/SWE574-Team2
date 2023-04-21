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

    title = models.CharField(max_length = 100)
    content = models.TextField(max_length = 500)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(default='')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    favourites = models.ManyToManyField(User, related_name='favourites', blank=True)
    tags = TaggableManager(blank=True)
    policy = models.CharField(max_length=10, choices=POLICY_CHOICES, default=PUBLIC)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-date_posted',)
