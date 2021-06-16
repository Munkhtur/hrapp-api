from django.db import models
from authentication.models import User

# Create your models here.


class Events(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    date = models.DateField()
    type = models.CharField(max_length=10, default='success')
