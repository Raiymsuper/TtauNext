from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientWithVideoViewSet,
    ClientWithoutVideoViewSet,
    VideoListView,
    ApplicationViewSet,
)



urlpatterns = [
    path('clients/with-videos/', ClientWithVideoViewSet.as_view(), name='clients-with-videos'),
    path('clients/without-videos/', ClientWithoutVideoViewSet.as_view(), name='clients-without-videos'),
    path('videos/', VideoListView.as_view(), name='videos'),
    path('applications/', ApplicationViewSet.as_view(), name='create-app'),
]
