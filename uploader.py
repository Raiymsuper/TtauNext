from minio import Minio
from minio.error import S3Error

def main():
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    source_file = "videostest/Ролик Здания.mp4"
    bucket_name = "python-test-bucket"
    destination_file = "Ролик Здания.mp4"

    # Ensure the bucket exists
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created bucket {bucket_name}")
    else:
        print(f"Bucket {bucket_name} already exists")

    client.fput_object(bucket_name, destination_file, source_file)
    print(f"{source_file} successfully uploaded to {bucket_name}/{destination_file}")

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("An error occurred:", exc)