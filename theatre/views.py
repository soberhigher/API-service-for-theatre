from rest_framework import viewsets

from theatre.models import (Play,
                            Actor,
                            Genre, TheatreHall
                            )
from theatre.permissions import IsAdminOrReadOnly
from theatre.serializers import (PlayReadSerializer,
                                 PlayWriteSerializer,
                                 ActorSerializer,
                                 GenreSerializer,
                                 TheatreHallSerializer
                                 )


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
