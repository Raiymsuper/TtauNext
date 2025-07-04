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
            file_obj = request.FILES['file']
            title = serializer.validated_data['title']
            bucket_name = settings.MINIO_MEDIA_BUCKET

            client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_USE_HTTPS
            )

            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)

            client.put_object(
                bucket_name,
                file_obj.name,
                file_obj,
                length=file_obj.size,
                content_type=file_obj.content_type
            )

            base_url = f"{'https' if settings.MINIO_USE_HTTPS else 'http'}://{settings.MINIO_ENDPOINT}"
            minio_url = f"{base_url}/{bucket_name}/{file_obj.name}"

            video = Video.objects.create(title=title, minio_url=minio_url)

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
