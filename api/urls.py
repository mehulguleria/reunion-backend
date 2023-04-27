from django.urls import path, include
from django.views.decorators.http import require_http_methods

from api import views


urlpatterns = [
    #authentication urls.
    path('',include('account.urls')),

    #user profile url.
    path('user',require_http_methods(['GET'])(views.UserAPIView.as_view()), name="userapi"),

    #post related urls.
    path('posts/',require_http_methods(['POST'])(views.PostAPIView.as_view()), name="createpostapi"),
    path('posts/<int:id>',require_http_methods(['GET','DELETE'])(views.PostAPIView.as_view()), name="getpostapi"),
    path('all_posts', require_http_methods(['GET'])(views.AllPostAPIView.as_view()), name="allpostapi"),

    #comment related urls.
    path('comment/<int:id>', require_http_methods(['POST'])(views.AddCommentAPIView.as_view()), name="addcomment"),

    #like and unlike urls.
    path('like/<int:id>',require_http_methods(['POST'])(views.LikePostAPIView.as_view()),name="likepost"),
    path('unlike/<int:id>',require_http_methods(['POST'])(views.DislikePostAPIView.as_view()),name="unlikepost"),

    #follow unfollow urls.
    path('follow/<int:id>',require_http_methods(['POST'])(views.FollowAPIView.as_view()),name="followuser"),
    path('unfollow/<int:id>',require_http_methods(['POST'])(views.UnFollowAPIView.as_view()),name="unfollowuser"),

]