from django.db import models

# Create your models here.

class Gender(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name