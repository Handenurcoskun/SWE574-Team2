from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Post
from spaces.models import Space
from django.db.models import Count, Avg

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='categories', blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def profiles_posts(self):
        return self.post_set.all()

    class Meta:
        ordering = ('-created',)

    def get_recommendations(self):
        spaces = Space.objects.filter(category__in=self.categories.all())
        recommendations = []
        for space in spaces:
            posts = space.posts.filter(policy=Post.PUBLIC)
            total_likes = sum(post.likes.count() for post in posts)
            if posts.count() >= 5 and (total_likes / posts.count()) >= 3:
                recommendations.append(space)
        return recommendations