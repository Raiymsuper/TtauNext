from rest_framework import serializers

from TtauNext import settings
from .models import *
from minio import Minio


class VideoUploadSerializer(serializers.Serializer):
    class Meta:
        model = Video
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'
