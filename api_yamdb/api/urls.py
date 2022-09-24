from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet,
                    CommentViewSet, UserViewSet, MeViewSet, create_user,
                    get_token)

auth_patterns = [
    path('signup/', create_user),
    path('token/', get_token)
]

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UserViewSet)
router.register("titles/(?P<title_id>\\d+)/reviews", ReviewViewSet, basename="reviews")
router.register("titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments",
                CommentViewSet,
                basename="comments"
                )

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/users/me/', MeViewSet.as_view()),
    path('v1/', include(router.urls)),
]
