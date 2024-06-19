from apps.users.models import User
from rest_framework import serializers


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "created_at"
        ]
