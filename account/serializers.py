from rest_framework import serializers

from image.serializers import UserProfileImageSerializer
from account.models import User


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'profile_image', 'username', 'name')


class UserProfileSerializer(serializers.ModelSerializer):
    images = UserProfileImageSerializer(many=True)
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id', 'profile_image', 'username', 'name', 'bio', 'website', 'post_count', 'followers_count', 'following_count', 'images')
