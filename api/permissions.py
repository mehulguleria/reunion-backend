from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated


class IsOwnerorReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if not request.user:
            raise NotAuthenticated('user not authenticated')
        
        if request.method in ['GET','HEAD','OPTION']:
            return True
        else:
            return obj.user == request.user
