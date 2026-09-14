from rest_framework import viewsets, serializers
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from django.utils import timezone

from theatre.models import (Play,
                            Actor,
                            Genre,
                            TheatreHall,
                            Performance,
                            Ticket
                            )
from theatre.permissions import IsAdminOrReadOnly
from theatre.serializers import (PlayReadSerializer,
                                 PlayWriteSerializer,
                                 ActorSerializer,
                                 GenreSerializer,
                                 TheatreHallSerializer,
    PerformanceReadSerializer,
                                  PerformanceWriteSerializer,
                                  RegistrationSerializer,
                                  TicketSerializer, TicketPurchaseSerializer
                                  )


class RegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


class PlayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Play.objects.all()

    def get_queryset(self):
        queryset = Play.objects.all()

        title = self.request.query_params.get("title")

        genres_id = self.request.query_params.get("genres")
        if genres_id:
            try:
                genres_id = [int(id) for id in genres_id.split(",")]
            except ValueError:
                raise ValidationError("Invalid genre ID format")

        actors_id = self.request.query_params.get("actors")
        if actors_id:
            try:
                actors_id = [int(id) for id in actors_id.split(",")]
            except ValueError:
                raise ValidationError("Invalid actor ID format")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genres_id:
            queryset = queryset.filter(genres__id__in=genres_id).distinct()
        if actors_id:
            queryset = queryset.filter(actors__id__in=actors_id).distinct()

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PlayReadSerializer
        return PlayWriteSerializer


class ActorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TheatreHallViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TheatreHallSerializer
    queryset = TheatreHall.objects.all()


class PerformanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Performance.objects.select_related(
        "play", "theatre_hall"
    ).prefetch_related("tickets")

    def get_queryset(self):
        queryset = self.queryset
        play_id = self.request.query_params.get("play")

        if play_id:
            try:
                play_id = [int(id) for id in play_id.split(",")]
            except ValueError:
                raise ValidationError("Invalid play ID format")

        theatre_hall_id = self.request.query_params.get("theatre_hall")

        if theatre_hall_id:
            try:
                theatre_hall_id = [int(id) for id in theatre_hall_id.split(",")]
            except ValueError:
                raise ValidationError("Invalid theatre hall ID format")

        show_date = self.request.query_params.get("date")

        if play_id:
            queryset = queryset.filter(play_id__in=play_id)
        if theatre_hall_id:
            queryset = queryset.filter(theatre_hall_id__in=theatre_hall_id)
        if show_date:
            queryset = queryset.filter(show_time__date=show_date)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PerformanceReadSerializer
        return PerformanceWriteSerializer


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()

    def get_queryset(self):
        return Ticket.objects.filter(reservation__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return TicketPurchaseSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        current_time = timezone.now()

        if instance.performance.show_time <= current_time:
            raise serializers.ValidationError(
                "Ticket cannot be cancelled after the performance has started"
            )

        reservation = instance.reservation
        instance.delete()

        if not reservation.tickets.exists():
            reservation.delete()

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
