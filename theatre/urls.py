from django.urls import path, include
from rest_framework.routers import DefaultRouter

from theatre.views import PlayViewSet


router = DefaultRouter()

router.register(r"plays", PlayViewSet)

urlpatterns = [
    path("", include(router.urls)),
]