from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class ClientWithVideoViewSet(APIView):
    def get(self, request):
        clients = Client.objects.filter(videos__isnull=False).distinct()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

class ClientWithoutVideoViewSet(APIView):
    def get(self, request):
        clients = Client.objects.filter(videos__isnull=True)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer