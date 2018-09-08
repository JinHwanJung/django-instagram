from django.db import models

from account.models import User
from base.models import TimeStampedModel


class Image(TimeStampedModel):
    file = models.ImageField()
    location = models.CharField(max_length=140)
    creator = models.ForeignKey(User, null=True, related_name='images', on_delete=models.PROTECT)
    caption = models.TextField()
