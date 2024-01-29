from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=250)
    slug=models.SlugField(unique=True)
   
class Massage(models.Model):
    room=models.ForeignKey(Room, related_name='message', on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='message', on_delete=models.CASCADE)
    content = models.TextField()
    date_added= models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering =('date_added', )
