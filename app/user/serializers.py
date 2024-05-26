"""
Serializers for the user API view
"""
from django.contrib.auth import ( # type: ignore # noqa
    get_user_model,
    authenticate
)
from rest_framework import serializers # type: ignore # noqa
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore # noqa
from django.utils.translation import gettext as _ # type: ignore # noqa
from django.http import JsonResponse # type: ignore # noqa
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore # noqa


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update & return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(TokenObtainPairSerializer):
    """Serializer for the auth token"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField(
            style={'input_type': 'password'},
            trim_whitespace=False,
        )

    def validate(self, attrs):
        """Validate and authenticate user"""
        super().validate(attrs)

        refresh = RefreshToken.for_user(self.user)

        return {
            'user_id': self.user.id,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
