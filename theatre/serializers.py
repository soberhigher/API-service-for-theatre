from rest_framework import serializers

from theatre.models import Play


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = "__all__"
