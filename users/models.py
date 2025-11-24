from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
