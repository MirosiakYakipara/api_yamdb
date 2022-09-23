from rest_framework import filters,  viewsets
from django.db.models import Avg

from titles.models import Title
from categories.models import Category
from genres.models import Genre


from .permissions import IsAdminOrReadOnly
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategorySerializer, GenreSerializer, 
                          TitleSerializer, ReadOnlyTitleSerializer)

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
        Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','category__slug','genre__slug',)

    def get_serializer_class(self):
        if self.action in ( 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer

