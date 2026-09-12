from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase

from theatre.models import Actor, Genre, Play




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




