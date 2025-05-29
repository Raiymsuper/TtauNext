from rest_framework import serializers
from .models import *
import tempfile
import os
from minio import Minio

class VideoUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    file = serializers.FileField()

    def create(self, validated_data):
        # Инициализация MinIO клиента
        client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )

        file_obj = validated_data['file']
        title = validated_data['title']
        bucket_name = "videos"

        # Создание бакета, если его нет
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        # Сохраняем временный файл
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file_obj.chunks():
                tmp.write(chunk)
            temp_path = tmp.name

        # Загрузка в MinIO
        client.fput_object(bucket_name, file_obj.name, temp_path)

        # Удаляем временный файл
        os.remove(temp_path)

        # Формируем публичный URL
        minio_url = f"http://localhost:9000/{bucket_name}/{file_obj.name}"

        # Сохраняем объект в БД
        return Video.objects.create(title=title, minio_url=minio_url)


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
