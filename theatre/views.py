from rest_framework import viewsets

from theatre.models import Play
from theatre.permissions import IsAdminOrReadOnly
from theatre.serializers import PlayReadSerializer, PlayWriteSerializer


class PlayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PlayReadSerializer
        return PlayWriteSerializer
