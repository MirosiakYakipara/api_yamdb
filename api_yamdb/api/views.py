from rest_framework import filters,  viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review


from .permissions import IsAdminOrReadOnly, UserPermission
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategorySerializer, GenreSerializer, 
                         TitleSerializer, ReadOnlyTitleSerializer)
from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review
from comments.models import Comment


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','category__slug','genre__slug',)

    def get_serializer_class(self):
            if self.action in ( 'list'):
                return ReadOnlyTitleSerializer
            return TitleSerializer


class ReviewViewSet(ListCreateDestroyViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"), title = self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    