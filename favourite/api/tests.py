from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
import json

from post.models import Post

from favourite.models import Favourite


class FavouriteCreateList(APITestCase):
    url = reverse("favourite:list-create")
    url_login = reverse("token_obtain_pair")

    def SetUp(self):
        self.username = "amilabdullazadeh"
        self.password = "webspace2020"
        self.post = Post.objects.create(title="Test", content="Test")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHENTIZATION="Bearer " + self.token)

    def test_add_favourite(self):
        data = {
            'content': "This is content for test",
            'user': self.user.id,
            'post': self.post.id
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_favourite(self):
        self.test_add_favourite()
        response = self.client.get(self.url)
        self.assertTrue(
            len(json.loads(response.content)["results"]) == Favourite.objects.filter(user=self.user).count())


class FavouriteUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def SetUp(self):
        self.username = "amilabdullazadeh"
        self.password = "webspace2020"
        self.post = Post.objects.create(title="Test", content="Test")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="ilmasefendi", password="codeacademy")
        self.favourite = Favourite.objects.create(content="test", post=self.post, user=self.user)
        self.url = reverse("favourite:update-delete", kwargs={'pk': self.favourite.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHENTIZATION="Bearer " + self.token)

    def test_fav_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_fav_delete_other(self):
        self.test_jwt_authentication("ilmasefendi")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_fav_update(self):
        data = {
            'content': "This is content for test",
            'user': self.user.id,
            'post': self.post.id
        }

        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favourite.objects.get(id=self.favourite.id).content == data['content'])

    def test_fav_update_others(self):
        self.test_jwt_authentication("ilmasefendi")
        data = {
            'content': "This is content for test",
            'user': self.user.id,
            'post': self.post.id
        }
        response = self.client.put(self.url, data)
        self.assertTrue(403, response.status_code)

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
