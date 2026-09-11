from rest_framework import viewsets

from theatre.models import Play
from theatre.permissions import IsAdminOrReadOnly
from theatre.serializers import PlaySerializer


class PlayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Play.objects.all()
    serializer_class = PlaySerializer
