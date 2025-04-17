from rest_framework import serializers
from .models import Application, Client, Video


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['method', 'contact', 'client_name', 'comment']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'video_file']


class ClientSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['client_name', 'logo', 'videos']
