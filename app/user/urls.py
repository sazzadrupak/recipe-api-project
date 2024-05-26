"""
URL mappings for the use API
"""
from django.urls import path # type: ignore # noqa
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token_obtain'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
