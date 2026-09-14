from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    TheatreHall,
)


class ActorGenrePlayTests(APITestCase):

    def setUp(self):
        self.actor = Actor.objects.create(first_name="John",
                                     last_name="Davidson")
        self.genre = Genre.objects.create(name="Comedy")
        play = Play.objects.create(title="King",
                                   description="Story of the King",)
        play.actors.add(self.actor)
        play.genres.add(self.genre)

    def test_anonymous_user_can_get_plays(self):
        url = reverse("play-list")
        response = self.client.get(url)
        res = response.data["results"]

        play_data = res[0]
        actor_data = res[0]["actors"][0]
        genre_data = res[0]["genres"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(play_data["title"], "King")
        self.assertEqual(actor_data["first_name"], "John")
        self.assertEqual(actor_data["last_name"], "Davidson")
        self.assertEqual(genre_data["name"], "Comedy")

    def test_staff_can_post_plays(self):
        url = reverse("play-list")
        user = get_user_model()
        staff_user = user.objects.create_user(username="admin",
                                              password="admin",
                                              is_staff=True)
        self.client.force_authenticate(user=staff_user)

        data = {
            "title": "Lion",
            "description": "Story about the biggest Lion",
            "actors": [self.actor.id],
            "genres": [self.genre.id],
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.count(), 2)

        created_play = Play.objects.get(title="Lion")
        self.assertIn(self.actor, created_play.actors.all())
        self.assertIn(self.genre, created_play.genres.all())


class TheatreHallTests(APITestCase):

    def setUp(self):
        self.theatrehall = TheatreHall.objects.create(name="City Big Hall",
                                                      rows=14,
                                                      seats_in_row=20)

    def test_anonymous_user_can_get_theatrehall(self):
        url = reverse("theatrehall-list")
        response = self.client.get(url)
        res = response.data["results"]
        theatrehall_data = res[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(theatrehall_data["name"], "City Big Hall")
        self.assertEqual(theatrehall_data["rows"], 14)
        self.assertEqual(theatrehall_data["seats_in_row"], 20)

    def test_staff_can_post_theatrehalls(self):
        url = reverse("theatrehall-list")
        user = get_user_model()
        staff_user = user.objects.create_user(username="admin", password="admin", is_staff=True)
        self.client.force_authenticate(user=staff_user)

        data = {
            "name": "City Big Hall",
            "rows": 11,
            "seats_in_row": 15,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TheatreHall.objects.count(), 2)


class PerformanceTests(APITestCase):
    def setUp(self):
        self.play = Play.objects.create(title="Big Ben",
                                        description="Show about Big Ben")
        self.theatre_hall = TheatreHall.objects.create(name="Big Hall",
                                                       rows=11,
                                                       seats_in_row=20)
        self.performance = Performance.objects.create(play=self.play,
                                                      theatre_hall=self.theatre_hall,
                                                      show_time="2026-09-20T11:50:00Z")

    def test_anonymous_user_can_get_performance(self):
        url = reverse("performance-list")
        response = self.client.get(url)
        res = response.data["results"]
        play_data = res[0]["play"]
        theatre_hall = res[0]["theatre_hall"]
        performance_data = res[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(play_data["title"], "Big Ben")
        self.assertEqual(play_data["description"], "Show about Big Ben")
        self.assertEqual(theatre_hall["name"], "Big Hall")
        self.assertEqual(theatre_hall["rows"], 11)
        self.assertEqual(theatre_hall["seats_in_row"], 20)
        self.assertEqual(performance_data["show_time"], "2026-09-20T11:50:00Z")

    def test_staff_can_post_performance(self):
        url = reverse("performance-list")
        user = get_user_model()
        staff_user = user.objects.create_superuser(username="admin",
                                                   password="admin")
        self.client.force_authenticate(user=staff_user)

        data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2026-09-20T13:50:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)
