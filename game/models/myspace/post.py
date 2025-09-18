from django.db import models
from django.utils.timezone import now

class Post(models.Model):
    user_id = models.IntegerField(default=0)
    content = models.TextField(default="", max_length=1000, blank=True, null=True)
    createtime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.content


