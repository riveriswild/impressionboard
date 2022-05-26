from django.db import models
import random

class Tweet(models.Model):
    # id - adds automatically when we save an image
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True) # blank - not required in django, null - not req in django AND in db

    class Meta:
        ordering = ['-id']     # needs migrations!

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
# Create your models here.
