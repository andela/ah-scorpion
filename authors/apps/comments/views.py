"""Define views for the comments app."""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from ..comments.models import Comment
from ..comments.serializers import CommentSerializer


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    """This view lists all comments in an article and also creates the comments."""

    # filter by slug from url
    lookup_field = 'article__slug'
    lookup_url_kwarg = 'slug'

    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def filter_queryset(self, queryset):
        """Handle getting comments on an article."""
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def get_serializer_context(self):
        """Interceptes request data and modifies it before passing it to the serialzer."""
        slug = self.kwargs['slug']
        context = super(CommentsListCreateAPIView,
                        self).get_serializer_context()
<<<<<<< HEAD
        context["request"].data.update({
            "slug": slug
        })
=======
        context["request"].data.update({"slug": slug})
>>>>>>> [Chore #159726516] Refactor to conform to PEP8
        return context


class CommentsCreateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView,
                                  generics.CreateAPIView):
    """This view updates and deletes a comment. It also creates a child to a comment."""

    lookup_url_kwarg = 'pk'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, slug=None, pk=None):
        """Handle deleting a comment."""
        try:
            pk = self.kwargs.get('pk')
        except self.kwargs.get('pk').DoesNotExist:
            raise NotFound('Please check your url')

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this id does not exist.')

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, slug=None, pk=None):
<<<<<<< HEAD
=======
        """Create a child comment on a parent comment."""
>>>>>>> [Chore #159726516] Refactor to conform to PEP8
        context = super(CommentsCreateDeleteAPIView,
                        self).get_serializer_context()
        try:
            slug = self.kwargs.get('slug')
        except self.kwargs.get('slug').DoesNotExist:
            raise NotFound('Please check your url')
        context["request"].data.update({"slug": slug})
        try:
            # getting the parent comment that will be the head of the thread
            context['request'].data['parent'] = Comment.objects.get(pk=pk).pk
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        serializer = self.serializer_class(
            data=context['request'].data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeComment(generics.UpdateAPIView):
    """
    Adds the user to the list of liking users and
    removes the user from the list of disliking users.
    If the user likes for a second time,
    we remove the user from the list of liking users.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def update(self, request, slug, pk):
        """Updates the user's liking status on a particular comment."""
        user = request.user

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this id does not exist.')

        # removes the user from the list of disliking users,
        # nothing changes if the user does not exist in the list of disliking users
        comment.dislikes.remove(user.id)

        # allows for the None option: you neither like nor dislike the comment
        if user in comment.likes.all():

            # removes the user from the list of liking users
            comment.likes.remove(user.id)

            response = {"Message": "You no longer like this comment"}
            return Response(response, status=status.HTTP_200_OK)

        # adds the user to the list of liking users
        comment.likes.add(user.id)

        response = {"Message": "You have successfully liked this comment"}
        return Response(response, status=status.HTTP_200_OK)


class DislikeComment(generics.UpdateAPIView):
    """
    Adds the user to the list of disliking users and
    removes the user from the list of liking users.
    If the user dislikes for a second time,
    we remove the user from the list of disliking users.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def update(self, request, slug, pk):
        """Updates the user's disliking status on a particular comment."""
        user = request.user

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this id does not exist.')

        # removes the user from the list of liking users,
        # nothing changes if the user does not exist in the list of liking users
        comment.likes.remove(user.id)

        # allows for the None option: you neither like nor dislike the comment
        if user in comment.dislikes.all():

            # removes the user from the list of disliking users
            comment.dislikes.remove(user.id)

            response = {"Message": "You no longer dislike this comment"}
            return Response(response, status=status.HTTP_200_OK)

        # adds the user to the list of disliking users
        comment.dislikes.add(user.id)

        response = {"Message": "You have successfully disliked this comment"}
        return Response(response, status=status.HTTP_200_OK)
