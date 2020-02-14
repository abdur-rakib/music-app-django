from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.urls import reverse

from django_extensions.db.fields import AutoSlugField


User = get_user_model()

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    artist = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='artist')
    album_title = models.CharField(max_length=50)
    album_logo = models.FileField()
    private = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"{self.album_title}({self.artist})"

    def get_absolute_url(self):
        return reverse('music:album_detail', kwargs={'slug': self.slug})

class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    song_title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='song_title')
    audio_file = models.FileField(default='')
    created = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.song_title
    

class FavouriteAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}({self.album})"

class FavouriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}({self.song})"