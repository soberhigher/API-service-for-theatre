from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import (PlayViewSet,
                           ActorViewSet,
                           GenreViewSet,
                           TheatreHallViewSet
                           )


router = DefaultRouter()

router.register(r"plays", PlayViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"theatre-halls", TheatreHallViewSet)

urlpatterns = [
    path("", include(router.urls)),
]