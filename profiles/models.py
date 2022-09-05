from django.db import models
from users.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UserId = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    name = models.fields.CharField(max_length=100,null=False)
    description = models.fields.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'