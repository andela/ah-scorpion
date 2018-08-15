from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from ..comments.models import Comment, CommentHistory
from ..comments.serializers import CommentSerializer, CommentHistorySerializer


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    """
    This view lists all comments in an article and also creates the comments
    """
    # filter by slug from url
    lookup_field = 'article__slug'
    lookup_url_kwarg = 'slug'
    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def get_serializer_context(self):
        slug = self.kwargs['slug']
        context = super(CommentsListCreateAPIView,
                        self).get_serializer_context()
        context["request"].data.update({
            "slug": slug
        })
        return context


class CommentsCreateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView,
                                  generics.CreateAPIView):
    lookup_url_kwarg = 'pk'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, slug=None, pk=None):
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
        context = super(CommentsCreateDeleteAPIView,
                        self).get_serializer_context()
        try:
            slug = self.kwargs.get('slug')
        except self.kwargs.get('slug').DoesNotExist:
            raise NotFound('Please check your url')
        context["request"].data.update({
            "slug": slug
        })
        try:
            # getting the parent comment that will be the head of the thread
            context['request'].data['parent'] = Comment.objects.get(pk=pk).pk
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')
        serializer = self.serializer_class(data=context['request'].data,
                                           context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug=None, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND)

        context = super(CommentsCreateDeleteAPIView,
                        self).get_serializer_context()
        new_comment = context["request"].data['content']

        initial_comment = comment.content

        if initial_comment == new_comment:
            return Response({"message": "New comment same as the existing. "
                                        "Editing rejected"},
                            status=status.HTTP_400_BAD_REQUEST)

        edited_comment = CommentHistory.objects.create(comment=initial_comment,
                                                       parent_comment=comment)
        edited_comment.save()

        comment.content = new_comment
        comment.save()

        serializer = self.serializer_class(data=context['request'].data,
                                           context=context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCommentHistory(generics.ListAPIView):
    lookup_url_kwarg = 'pk'
    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Overrides the default GET request from ListAPIView
        Returns all comment edits for a particular comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        # """

        try:
            comment = Comment.objects.get(pk=kwargs['pk'])
        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND)

        self.queryset = CommentHistory.objects.filter(parent_comment=comment)

        return generics.ListAPIView.list(self, request, *args, **kwargs)
