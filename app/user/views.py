"""
Views for the user API
"""
from rest_framework import generics, permissions # type: ignore # noqa
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore # noqa
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore # noqa
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    """Create token for valid user"""
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve & return the authenticated user"""
        return self.request.user
