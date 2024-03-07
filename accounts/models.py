from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(null=True, blank=True, max_length=200)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)
    
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        return self.user.username