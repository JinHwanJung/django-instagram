from rest_framework.serializers import ModelSerializer

from account.serializers import ListUserSerializer
from image.serializers import SamllImageSerializer, CommentSerializer
from notification.models import Notification


class NotificationSerializer(ModelSerializer):
    creator = ListUserSerializer()
    image = SamllImageSerializer()
    comment = CommentSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
