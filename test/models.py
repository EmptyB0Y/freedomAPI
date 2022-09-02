from django.db import models

class Player(models.Model):
    name = models.fields.CharField(max_length=100)
    #test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'