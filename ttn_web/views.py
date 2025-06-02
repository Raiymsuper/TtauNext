from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

from django.http import JsonResponse
from minio import Minio
from minio.error import S3Error
import tempfile

# Connect to MinIO
minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

class VideoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response({
                "id": video.id,
                "title": video.title,
                "minio_url": video.minio_url,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# Добавить в модельку бланк на играет и не играет
class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class ApplicationViewSet(APIView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Application created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
