from django.db import models
from authentication.models import User

# Create your models here.


class Attendance(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,  default="", editable=False)
    email = models.EmailField(max_length=30,  default="", editable=False)
    department = models.CharField(max_length=30, default='')
    clockin = models.DateField()
    clockout = models.DateField()
    workhours = models.FloatField()
    breakhours = models.FloatField()
    status = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.name = self.owner.full_name
        self.email = self.owner.email
        self.department = self.owner.department
        super(Attendance, self).save(*args, **kwargs)
