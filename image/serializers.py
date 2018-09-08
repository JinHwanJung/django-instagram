from rest_framework import serializers

from account.models import User
from image.models import Image, Comment, Like


class SamllImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('file', )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'profile_image'
        )


class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'message', 'creator', )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = Image
        fields = (
            'id', 'file', 'location', 'creator', 'caption', 'like_count', 'comments', 'created_date',
        )


class UserProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'file', 'like_count', 'comment_count')


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('file', 'location', 'creator', 'caption')
