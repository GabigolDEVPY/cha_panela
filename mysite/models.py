from django.db import models

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Nome: {self.name}"