from rest_framework import serializers
from api.models import (Post, Comment)
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    follower = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id','email','username','follower','following')

    def get_follower(self,obj):
        return obj.following.count()

    def get_following(self,obj):
        return obj.follower.count()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text','user','created_at')
        extra_kwargs = {
            "created_at":{"read_only":True}
        }

    def create(self, validated_data):
        user = validated_data['user']
        text = validated_data['text']
        post = Post.objects.get(id=validated_data['id'])
        comment = Comment(user=user, text=text, post=post)
        comment.save()
        return comment


class PostSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "created_at":{"read_only":True}
        }

    def create(self, validated_data,**kwargs):
        title = validated_data['title']
        description = validated_data['description']
        user = validated_data['user']
        post = Post(title=title, description=description, user=user)
        post.save()
        return post

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSerializer(comments, many=True, read_only=True)
        return serializer.data

    