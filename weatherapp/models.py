from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.TextField(default='', max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'owner')

    def __str__(self):
        return self.name