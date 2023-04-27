from django.urls import path
from account.views import UserLogin

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('authenticate', UserLogin.as_view(), name='token_obtain_pair'),
    path('authenticate/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]