from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from users.models import Category


class Space(models.Model):

    PUBLIC = 'public'
    PRIVATE = 'private'

    POLICY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length = 100, unique=True)
    description = models.TextField(max_length = 500)
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_spaces')
    policy = models.CharField(max_length=10, choices=POLICY_CHOICES, default=PUBLIC)
    members = models.ManyToManyField(User, through='SpaceMembership', related_name='spaces', blank=True)
    image = models.ImageField(default='space_default.jpg', upload_to='space_pics')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('space-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-date_created',)




class SpaceMembership(models.Model):
    OWNER = 'owner'
    BASIC_MEMBER = 'basic_member'
    PRO_MEMBER = 'pro_member'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (BASIC_MEMBER, 'Basic Member'),
        (PRO_MEMBER, 'Pro Member'),
        (MODERATOR, 'Moderator'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=BASIC_MEMBER)

    def is_owner(self):
        return self.role == SpaceMembership.OWNER

    def is_moderator(self):
        return self.role == SpaceMembership.MODERATOR

    def is_pro_member(self):
        return self.role == SpaceMembership.PRO_MEMBER

    def is_basic_member(self):
        return self.role == SpaceMembership.BASIC_MEMBER


    class Meta:
        unique_together = ('user', 'space')

class PrivateSpaceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)