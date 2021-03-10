from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from movie.models import LikeDislikeOption


class TestUrls(TestCase):

    def setUp(self):
        User.objects.create_user(username="test1@test.com", password="test123")
        self.like_url = reverse('like')
        self.login_url = reverse('login')
        response = self.client.post(self.login_url, {'email': 'test1@test.com', 'password': 'test123'})
        print(response)
        self.user = response.data['user']
        self.token = response.data['token']

    def test_like_error_user(self):
        LikeDislikeOption.objects.create(user_id="test1@test.com", movie_id="1",type=True)

        response = self.client.post(self.like_url, {
            "movie_id": "1",
            "type": "True"
        }, HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 405)

    def test_like_success_user(self):
        response = self.client.post(self.like_url, {
            "movie_id": "3",
            "type": "True"
        }, HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
