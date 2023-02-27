from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)


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
