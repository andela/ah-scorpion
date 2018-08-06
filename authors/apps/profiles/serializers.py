from rest_framework import serializers

from authors.apps.authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects to return
    their profile alone"""

    class Meta:
        model = User
        fields = ('email', 'username', 'bio', 'image')
