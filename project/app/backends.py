# Django
from django.contrib.auth.backends import ModelBackend

# Local
from .models import User


class Auth0Backend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs.get('username', None)
        name = kwargs.get('name', '(Unknown)')
        email = kwargs.get('email', None)
        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            user = User(
                username=username,
                name=name,
                email=email,
            )
            user.set_unusable_password()
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
