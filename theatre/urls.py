from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    TicketViewSet,
)


router = DefaultRouter()

router.register(r"plays", PlayViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"theatre-halls", TheatreHallViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
