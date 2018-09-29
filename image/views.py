from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import ListUserSerializer
from image.models import Image, Like, Comment
from image.serializers import ImageSerializer, InputImageSerializer, CommentSerializer, UserProfileImageSerializer


class Images(APIView):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        all_following_users = user.following.all()
        feed_images = []

        for following_user in all_following_users:
            for image in following_user.images.all()[:2]:
                feed_images.append(image)
        my_images = user.images.all()[:2]
        for image in my_images:
            feed_images.append(image)

        sorted_list = sorted(feed_images, key=lambda image: image.created_date, reverse=True)
        serializer = ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = InputImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):

    def find_own_image(self, user, image_id):
        try:
            found_image = Image.objects.get(id=image_id, creator=user)
            return found_image
        except Image.DoesNotExist:
            return None

    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUESTT)
        serializer = ImageSerializer(image)
        return Response(data=serializer.data, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, image_id):
        user = request.user
        image = self.find_own_image(user, image_id)
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = InputImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id):
        user = request.user
        image = self.find_own_image(user, image_id)
        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeImage(APIView):
    def get(self, request, image_id):
        image = Image.objects.get(id=image_id)
        users = [image.creator for image in image.likes.all()]
        serializer = ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id):
        user = request.user
        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            Like.objects.get(creator=user, image=found_image)
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except Like.DoesNotExist:
            like = Like.objects.create(creator=user, image=found_image)
            found_image.new_like_notify(like)
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, image_id):
        user = request.user
        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = Like.objects.get(creator=user, image=found_image)
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id):
        user = request.user
        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(creator=user, image=found_image)
            found_image.new_comment_notify(comment)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    def delete(self, request, comment_id):
        user = request.user
        try:
            found_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if found_comment.creator != user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            found_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class Search(APIView):

    def get(self, request):
        hashtags = request.query_params.get('hashtags', None)
        if hashtags is not None:
            tags = hashtags.split(',')
            images = Image.objects.filter(tags__name__in=tags).distinct()
            serializer = UserProfileImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModerateComment(APIView):
    def delete(self, request, image_id, comment_id):
        user = request.user
        try:
            comment_to_delete = Comment.objects.get(id=comment_id, image=image_id, image__creator=user)
            comment_to_delete.delete()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
