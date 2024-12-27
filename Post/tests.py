from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Post.models import (
    Post,
    Comment,
    LikedPost,
    DisLikedPost,
    LikedComment,
    DisLikedComment,
)
from django.http import JsonResponse


class PostInteractionTests(TestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Create a post
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", author=self.user1
        )
        self.comment = Comment.objects.create(
            content="Test comment", author=self.user1, parent_post=self.post
        )

        # Log in as user1
        self.client.login(username="user1", password="password123")

    def test_like_post(self):
        url = reverse("like-toggle", kwargs={"post_id": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "like_added", "likes_count": 1}
        )

        # Simulate liking again (should remove the like)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "like_removed", "likes_count": 0}
        )

    def test_dislike_post(self):
        url = reverse("dislike-toggle", kwargs={"post_id": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "dislike_added", "dislikes_count": 1}
        )

        # Simulate disliking again (should remove the dislike)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "dislike_removed", "dislikes_count": 0}
        )

    def test_like_comment(self):
        url = reverse("like-comment-toggle", kwargs={"comment_id": self.comment.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "like_added", "likes_count": 1}
        )

        # Simulate liking again (should remove the like)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "like_removed", "likes_count": 0}
        )

    def test_dislike_comment(self):
        url = reverse("dislike-comment-toggle", kwargs={"comment_id": self.comment.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "dislike_added", "dislikes_count": 1}
        )

        # Simulate disliking again (should remove the dislike)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"status": "dislike_removed", "dislikes_count": 0}
        )

    def test_like_post_own_post(self):
        self.client.login(username="user1", password="password123")
        url = reverse("like-toggle", kwargs={"post_id": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "You cannot like your own post."}
        )

    def test_dislike_post_own_post(self):
        self.client.login(username="user1", password="password123")
        url = reverse("dislike-toggle", kwargs={"post_id": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "You cannot dislike your own post."}
        )

    def test_like_comment_own_comment(self):
        self.client.login(username="user1", password="password123")
        url = reverse("like-comment-toggle", kwargs={"comment_id": self.comment.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "You cannot like your own comment."}
        )

    def test_dislike_comment_own_comment(self):
        self.client.login(username="user1", password="password123")
        url = reverse("dislike-comment-toggle", kwargs={"comment_id": self.comment.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "You cannot dislike your own comment."}
        )
