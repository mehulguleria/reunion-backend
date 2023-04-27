from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.serializer import PostSerializer,CommentSerializer, UserSerializer
from api.models import (Post, Like, Follower)
from api.permissions import IsOwnerorReadOnly
from account.models import User

from django.core.exceptions import ObjectDoesNotExist


class UserAPIView(APIView):
    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())
    
    def get(self,request):
        self.check_permissions(request)
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class FollowAPIView(APIView):
    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())
    
    def post(self,request,id):
        self.check_permissions(request)
        if request.user == User.objects.get(id=id):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        Follower.objects.get_or_create(user=request.user,follower=User.objects.get(id=id))
        return Response(status=status.HTTP_200_OK)
    

class UnFollowAPIView(APIView):
    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())
    
    def post(self,request,id):
        self.check_permissions(request)
        try:
            Follower.objects.get(user=request.user, follower=User.objects.get(id=id)).delete()
            return Response(status=status.HTTP_200_OK) 
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class LikePostAPIView(APIView):

    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())

    def post(self,request,id):
        self.check_permissions(request)
        Like.objects.get_or_create(post=Post.objects.get(id=id),user=request.user)
        return Response(status=status.HTTP_200_OK)


class DislikePostAPIView(APIView):

    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())

    def post(self,request,id):
        self.check_permissions(request)
        try:
            Like.objects.get(post=Post.objects.get(id=id),user=request.user).delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AddCommentAPIView(APIView):

    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())
    
    def post(self,request,id):
        self.check_permissions(request)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=id, user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class AllPostAPIView(APIView):

    def get_permissions(self):
        return (IsOwnerorReadOnly(),IsAuthenticated())

    def get(self,request):
        self.check_permissions(request)
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostAPIView(APIView):

    def get_permissions(self):
        if self.request.method in ["GET","POST","DELETE"]:
            return [IsOwnerorReadOnly(), IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def get(self, request, id):
        self.check_permissions(request)
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def delete(self, request, id):
        self.check_permissions(request)
        post = Post.objects.get(id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

