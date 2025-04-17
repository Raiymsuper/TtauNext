from django.db import models

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    client_name = models.CharField(max_length=60)
    comment = models.TextField()

    def __str__(self):
        return self.client_name


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/')
    videos = models.ManyToManyField(Video, blank=True)

    def __str__(self):
        return self.client_name