from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(blank=True, max_length=255)
    website = models.URLField(null=True)
    bio = models.TextField(null=True)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    following = models.ManyToManyField("self", related_name="+")
    follower = models.ManyToManyField("self", related_name="+")
    profile_image = models.ImageField(null=True)

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.follower.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def post_count(self):
        return self.images.count()

    def new_follow_notify(self, user):
        from notification.models import Notification
        Notification.objects.create(creator=user, to=self, notification_type='follow')
