from rest_framework import serializers

from theatre.models import Play, Actor, Genre, TheatreHall, Performance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PlayReadSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = "__all__"


class PerformanceReadSerializer(serializers.ModelSerializer):
    theatre_hall = TheatreHallSerializer(read_only=True)
    play = PlayReadSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = "__all__"


class PerformanceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = "__all__"