from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from theatre.models import (Play,
                            Actor,
                            Genre,
                            TheatreHall,
                            Performance,
                            Reservation
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
                                 ReservationSerializer
                                 )


class RegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


class PlayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Play.objects.all()

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
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PerformanceReadSerializer
        return PerformanceWriteSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)