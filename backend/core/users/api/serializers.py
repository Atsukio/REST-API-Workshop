from rest_framework import serializers

from core.users.models import ToDo, User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = "__all__"
