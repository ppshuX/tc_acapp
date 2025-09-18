from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    source = models.IntegerField(default=0)
    target = models.IntegerField(default=0)

    def __str__(self):
        return str(self.source) + ' - ' + str(self.target)

