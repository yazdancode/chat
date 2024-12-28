from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from Post.models import (
    Comment,
    DisLikedComment,
    DisLikedPost,
    DisLikedReply,
    LikedComment,
    LikedPost,
    LikedReply,
    Post,
    Reply,
)


class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get("post_id"))

        if post.author == request.user:
            return JsonResponse({"error": "You cannot like your own post."}, status=400)

        user_liked = post.likes.filter(id=request.user.id).exists()

        if user_liked:
            LikedPost.objects.filter(user=request.user, post=post).delete()
            return JsonResponse(
                {"status": "like_removed", "likes_count": post.likes.count()}
            )
        else:
            LikedPost.objects.create(user=request.user, post=post)
            return JsonResponse(
                {"status": "like_added", "likes_count": post.likes.count()}
            )


class DisLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get("post_id"))

        if post.author == request.user:
            return JsonResponse(
                {"error": "You cannot dislike your own post."}, status=400
            )

        user_disliked = post.dislikes.filter(id=request.user.id).exists()

        if user_disliked:
            DisLikedPost.objects.filter(user=request.user, post=post).delete()
            return JsonResponse(
                {"status": "dislike_removed", "dislikes_count": post.dislikes.count()}
            )
        else:
            DisLikedPost.objects.create(user=request.user, post=post)
            return JsonResponse(
                {"status": "dislike_added", "dislikes_count": post.dislikes.count()}
            )


class LikedCommentToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get("comment_id"))
        if comment.author == request.user:
            return JsonResponse(
                {"error": "You cannot like your own comment."}, status=400
            )

        user_liked = comment.likes.filter(id=request.user.id).exists()
        if user_liked:
            LikedComment.objects.filter(user=request.user, comment=comment).delete()
            return JsonResponse(
                {"status": "like_removed", "likes_count": comment.likes.count()}
            )
        else:
            LikedComment.objects.create(user=request.user, comment=comment)
            return JsonResponse(
                {"status": "like_added", "likes_count": comment.likes.count()}
            )


class DisLikedCommentToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get("comment_id"))
        if comment.author == request.user:
            return JsonResponse(
                {"error": "You cannot dislike your own comment."}, status=400
            )

        user_disliked = comment.dislikes.filter(id=request.user.id).exists()
        if user_disliked:
            DisLikedComment.objects.filter(user=request.user, comment=comment).delete()
            return JsonResponse(
                {
                    "status": "dislike_removed",
                    "dislikes_count": comment.dislikes.count(),
                }
            )
        else:
            DisLikedComment.objects.create(user=request.user, comment=comment)
            return JsonResponse(
                {"status": "dislike_added", "dislikes_count": comment.dislikes.count()}
            )


class LikedReplyToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get("post_id"))
        if post.author == request.user:
            return JsonResponse({"error": "You cannot like your own post."}, status=400)
        user_liked = post.likes.filter(id=request.user.id).exists()
        if user_liked:
            LikedReply.objects.filter(user=request.user, post=post).delete()
            return JsonResponse(
                {"status": "like_removed", "likes_count": post.likes.count()}
            )
        else:
            LikedReply.objects.create(user=request.user, post=post)
            return JsonResponse(
                {"status": "like_added", "likes_count": post.likes.count()}
            )


class DisLikedReplyToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Reply, id=kwargs.get("comment_id"))
        if comment.author == request.user:
            return JsonResponse(
                {"error": "You cannot dislike your own comment."}, status=400
            )

        user_disliked = comment.dislikes.filter(id=request.user.id).exists()
        if user_disliked:
            DisLikedReply.objects.filter(user=request.user, comment=comment).delete()
            return JsonResponse(
                {
                    "status": "dislike_removed",
                    "dislikes_count": comment.dislikes.count(),
                }
            )
        else:
            DisLikedReply.objects.create(user=request.user, comment=comment)
            return JsonResponse(
                {"status": "dislike_added", "dislikes_count": comment.dislikes.count()}
            )
