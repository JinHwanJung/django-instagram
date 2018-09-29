from django.urls import path

from image.views import Images, ModerateComment, CommentOnImage, LikeImage, ImageDetail, CommentView, Search

app_name = "image"

urlpatterns = [
    path('', Images.as_view(), name='feeds'),
    path('<int:image_id>/', ImageDetail.as_view(), name='feeds'),
    path('<int:image_id>/likes/', LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/comments/', CommentOnImage.as_view(), name='comment_image'),
    path('<int:image_id>/comments/<int:comment_id>/', ModerateComment.as_view(), name='comment_image'),
    path('comments/<int:comment_id>/', CommentView.as_view(), 'name=comment_delete'),
    path('search/', Search.as_view(), name='image_search'),
]
