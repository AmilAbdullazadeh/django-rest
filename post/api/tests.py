from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.templatetags.rest_framework import data
from rest_framework.test import APITestCase
import json

from post.models import Post


class PostCreateList(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:list")
    url_login = reverse("token_obtain_pair")

    def SetUp(self):
        self.username = "amilabdullazadeh"
        self.password = "webspace2020"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHENTIZATION="Bearer " + self.token)

    def test_add_post(self):
        data = {
            'content': "This is content for test",
            'user': self.user.id,
        }

        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_add_new_post_unauthorization(self):
        self.client.credentials()
        data = {
            'content': "This is content for test",
            'title': "test"
        }

        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)

    def test_posts(self):
        self.test_add_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)['results']) == Post.objects.all().count())


class PostUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def SetUp(self):
        self.username = "amilabdullazadeh"
        self.password = "webspace2020"
        self.post = Post.objects.create(title="Test", content="Test")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="ilmasefendi", password="codeacademy")
        self.post = Post.objects.create(title="test", content="test")
        self.url = reverse("post:update", kwargs={'slug': self.post.slug})
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHENTIZATION="Bearer " + self.token)

    def test_post_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_delete_post_others(self):
        self.test_jwt_authentication("ilmasefendi")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_update_post(self):
        response = self.client.put(self.url, data={'content': "Test", 'title': "test"})
        self.assertEqual(200, response.status_code)
        self.assertTrue(Post.object.get(pk=self.post.pk).content == data['content'])

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
