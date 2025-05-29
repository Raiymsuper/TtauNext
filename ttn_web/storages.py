from minio_storage.storage import MediaCloudStorage

class VideoStorage(MediaCloudStorage):
    bucket_name = "videos"

class LogoStorage(MediaCloudStorage):
    bucket_name = "logos"