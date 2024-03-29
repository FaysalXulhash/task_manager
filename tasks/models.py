from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=((1, 'Low'), (2, 'Medium'), (3, 'High')), default=1)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("task-list")


class Photo(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.image.name
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)