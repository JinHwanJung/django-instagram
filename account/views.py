from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import ListUserSerializer, UserProfileSerializer


class ExploreUsers(APIView):
    def get(self, request):
        last_five_users = User.objects.order_by('-date_joined')[:5]
        serializer = ListUserSerializer(last_five_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):
    def post(self, request, user_id):
        user = request.user
        try:
            found_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.add(found_user)
        found_user.new_follow_notify(user)
        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    def post(self, request, user_id):
        user = request.user
        try:
            found_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.remove(found_user)
        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):
    def get_user(self, username):
        try:
            found_user = User.objects.get(username=username)
            return found_user
        except User.DoesNotExist:
            return None

    def get(self, request, username):
        found_user = self.get_user(username)
        if not found_user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(found_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        found_user = self.get_user(username)
        if not found_user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif found_user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = UserProfileSerializer(found_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowers(APIView):
    def get(self, request, username):
        try:
            found_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_followers = found_user.follower.all()
        serializer = ListUserSerializer(user_followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowings(APIView):
    def get(self, request, username):
        try:
            found_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_followings = found_user.following.all()
        serializer = ListUserSerializer(user_followings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):
    def get(self, request):
        username = request.query_params.get("username", None)
        if username is not None:
            users = User.objects.filter(username__icontains=username)
            serializer = ListUserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def put(self, request, username):
        user = request.user
        if user.username != username:
            return Response(status.HTTP_401_UNAUTHORIZED)

        current_password = request.data.get("current_password", None)
        new_password = request.data.get("new_password", None)

        if not current_password and current_password != 0:
            return Response(status.HTTP_400_BAD_REQUEST)

        if not new_password and new_password != 0:
            return Response(status.HTTP_400_BAD_REQUEST)

        is_correct = user.check_password(current_password)

        if is_correct:
            user.set_password(new_password)
            user.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
