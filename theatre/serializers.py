from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from theatre.models import (Play,
                            Actor,
                            Genre,
                            TheatreHall,
                            Performance,
                            Reservation,
                            Ticket
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


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["id", "reservation"]


class TicketPurchaseSerializer(serializers.Serializer):
    tickets = TicketSerializer(many=True)

    def validate_tickets(self, tickets):
        if not tickets:
            raise serializers.ValidationError(
                "Purchase must contain at least one ticket"
            )
        selected_places = set()

        for ticket in tickets:
            performance = ticket["performance"]
            row = ticket["row"]
            seat = ticket["seat"]
            hall = performance.theatre_hall

            place = (performance.id, row, seat)

            if Ticket.objects.filter(
                    performance=performance,
                    row=row,
                    seat=seat
            ).exists():
                raise serializers.ValidationError(
                    "This seat is already reserved"
                )

            if place in selected_places:
                raise serializers.ValidationError(
                    "The same seat cannot be selected more than once."
                )
            selected_places.add(place)

            if row < 1 or row > hall.rows:
                raise serializers.ValidationError(
                    f"Row must be between 1 and {hall.rows}"
                )
            if seat < 1 or seat > hall.seats_in_row:
                raise serializers.ValidationError(
                    f"Seat must be between 1 and {hall.seats_in_row}."
                )

        return tickets

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        user = validated_data["user"]

        reservation = Reservation.objects.create(user=user)

        created_tickets = []
        for ticket_data in tickets_data:
            ticket = Ticket.objects.create(
                reservation=reservation,
                **ticket_data,
            )
            created_tickets.append(ticket)

        return created_tickets


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "tickets"]
        read_only_fields = ["id", "created_at", "user"]

    def validate_tickets(self, tickets):
        if not tickets:
            raise serializers.ValidationError(
                "Reservation must contain at least one ticket"
            )
        selected_places = set()

        for ticket in tickets:
            performance = ticket["performance"]
            row = ticket["row"]
            seat = ticket["seat"]
            hall = performance.theatre_hall

            place = (performance.id, row, seat)

            if Ticket.objects.filter(
                performance=performance,
                row=row,
                seat=seat
            ).exists():
                raise serializers.ValidationError(
                    "This seat is already reserved"
                )

            if place in selected_places:
                raise serializers.ValidationError(
                    "The same seat cannot be selected more than once."
                )
            selected_places.add(place)

            if row < 1 or row > hall.rows:
                raise serializers.ValidationError(
                    f"Row must be between 1 and {hall.rows}"
                )
            if seat < 1 or seat > hall.seats_in_row:
                raise serializers.ValidationError(
                    f"Seat must be between 1 and {hall.seats_in_row}."
                )

        return tickets

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")

        reservation = Reservation.objects.create(
            **validated_data,
        )

        for ticket_data in tickets_data:
            Ticket.objects.create(
                reservation=reservation,
                **ticket_data,
            )
        return reservation