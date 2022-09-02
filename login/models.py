from django.db import models
from django.core.validators import EmailValidator

class User(models.Model):
    name = models.fields.CharField(max_length=100)
    email = models.fields.CharField(max_length=200,validators=[EmailValidator],unique=True)
    password = models.fields.CharField(max_length=100)
    isConfirmed = models.fields.BooleanField(default=False)
    confirmationKey = models.fields.CharField(max_length=100,null=True)

    def __str__(self):
        return f'{self.name}'