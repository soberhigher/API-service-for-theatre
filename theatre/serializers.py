from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from theatre.models import (Play,
                            Actor,
                            Genre,
                            TheatreHall,
                            Performance, Reservation
                            )

from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    confirm_password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password", "date_joined"]

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        validate_password(
            attrs["password"],
            user=User(username=attrs["username"])
        )

        return attrs

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value



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


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user"]