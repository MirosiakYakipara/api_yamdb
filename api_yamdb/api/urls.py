from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register("titles/(?P<title_id>\\d+)/reviews", ReviewViewSet, basename="reviews")
router.register("titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments",
                CommentViewSet,
                basename="comments"
                )

urlpatterns = [
    path('v1/', include(router.urls)),
]
