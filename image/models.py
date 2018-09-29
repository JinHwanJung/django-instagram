from django.db import models
from taggit.managers import TaggableManager

from account.models import User
from base.models import TimeStampedModel


class Image(TimeStampedModel):
    class Meta:
        ordering = ['-created_date']

    file = models.ImageField()
    location = models.CharField(max_length=140)
    creator = models.ForeignKey(User, null=True, related_name='images', on_delete=models.PROTECT)
    caption = models.TextField()
    tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Comment(TimeStampedModel):
    message = models.TextField()
    creator = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, null=True, related_name='comments', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return "{}".format(self.message)


class Like(TimeStampedModel):

    creator = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, null=True, related_name='likes', on_delete=models.PROTECT)

    def __str__(self):
        return "User: {} - Image Caption: {}".format(self.creator.username, self.image.caption)
