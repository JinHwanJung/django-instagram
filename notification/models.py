from django.db import models

from account.models import User
from image.models import Image, Comment


class Notification(models.Model):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    creator = models.ForeignKey(User, related_name='notifications_by_creator', on_delete=models.PROTECT)
    to = models.ForeignKey(User, related_name='notifications_by_to', on_delete=models.PROTECT)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(Image, related_name='+', null=True, blank=True, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, related_name='+', null=True, blank=True, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.is_valid(self.creator, self.to, self.notification_type, self.image, self.comment):
            super().save(*args, **kwargs)

    @classmethod
    def is_valid(cls, creator, to, notification_type, image=None, comment=None):
        if not isinstance(creator, User):
            return False
        if not isinstance(to, User):
            return False
        if image and not isinstance(image, Image):
            return False
        if comment and not isinstance(comment, Comment):
            return False

        if notification_type == 'like':
            if not (image or comment):
                return False
        elif notification_type == 'comment':
            if image:
                return False
            elif not comment:
                return False
        elif notification_type == 'follow':
            if image or comment:
                return False
        else:
            return False

        if creator == to:
            return False
        if image and image.creator != to:
            return False
        if comment and comment.creator != creator:
            return False
        if comment and comment.image.creator != to:
            return False
        return True
