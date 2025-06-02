from rest_framework import serializers

from TtauNext import settings
from .models import *
from minio import Minio


class VideoUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    file = serializers.FileField()

    def create(self, validated_data):
        file_obj = validated_data['file']
        title = validated_data['title']
        bucket_name = settings.MINIO_MEDIA_BUCKET

        # Инициализация клиента MinIO
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_HTTPS
        )

        # Создание бакета при необходимости
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        # Загрузка файла напрямую из потока
        client.put_object(
            bucket_name,
            file_obj.name,
            file_obj,
            length=file_obj.size,
            content_type=file_obj.content_type
        )

        # Формирование ссылки (можно использовать публичную или временную)
        if settings.MINIO_USE_HTTPS:
            base_url = f"https://{settings.MINIO_ENDPOINT}"
        else:
            base_url = f"http://{settings.MINIO_ENDPOINT}"

        # Вариант 1: прямая ссылка (если бакет публичен)
        minio_url = f"{base_url}/{bucket_name}/{file_obj.name}"

        # Вариант 2: временная ссылка (если бакет закрыт)
        # minio_url = client.presigned_get_object(bucket_name, file_obj.name, expires=timedelta(hours=1))

        # Сохраняем в базу
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
