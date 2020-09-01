from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
import json

from post.models import Post
from comment.models import Comment


class CommentUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def SetUp(self):
        self.username = "amilabdullazadeh"
        self.password = "webspace2020"
        self.post = Post.objects.create(title="Test", content="Test")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="ilmasefendi", password="codeacademy")
        self.comment = Comment.objects.create(content="test", post=self.post, user=self.user)
        self.url = reverse("comment:update", kwargs={'pk': self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHENTIZATION="Bearer " + self.token)

    def test_comment_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Comment.object.filter(pk=self.comment.pk).exists)

    def test_delete_comment_others(self):
        self.test_jwt_authentication("ilmasefendi")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.object.get(pk=self.comment.pk))

    def test_update_comment(self):
        response = self.client.put(self.url, data={'content': "Test"})
        self.assertEqual(200, response.status_code)
        self.assertTrue(Comment.object.get(pk=self.comment.pk).content, "Test")

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
