import http

from articles.models import Article
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Comment

User = get_user_model()


class TestAddCommentView(TestCase):
    password = "testpass"

    @classmethod
    def setUpTestData(cls):

        cls.author = User(
            email="tester@gmail.com",
            name="tester",
        )
        cls.author.set_password(cls.password)
        cls.author.save()

        cls.article = Article.objects.create(
            title="test",
            summary="test",
            content="test",
            author=cls.author,
        )

        cls.url = reverse("add_comment", args=[cls.article.id])

    def test_add_comment(self):
        self.client.login(email=self.author.email, password=self.password)

        response = self.client.post(self.url, {"content": "test"})
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        comment = Comment.objects.get()

        self.assertEqual(comment.article, self.article)
        self.assertEqual(comment.author, self.author)
