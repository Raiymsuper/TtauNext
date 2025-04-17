from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientWithVideoViewSet,
    ClientWithoutVideoViewSet,
    VideoListView,
    ApplicationViewSet,
)

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('clients/with-videos/', ClientWithVideoViewSet.as_view(), name='clients-with-videos'),
    path('clients/without-videos/', ClientWithoutVideoViewSet.as_view(), name='clients-without-videos'),
    path('videos/', VideoListView.as_view(), name='videos'),
    path('', include(router.urls)),
]
