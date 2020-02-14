from django.urls import path, include
from .views import *

app_name = 'music'

urlpatterns = [
    path('', AlbumView.as_view(), name='album'),
    path('create/album/', AlbumCreateView.as_view(), name='album_create'),
    path('create/song/<slug>/', SongCreateView.as_view(), name='song_create'),
    path('albums/<slug>/', AlbumDetailView.as_view(), name='album_detail'),
    path('<slug>/delete/album/', delete_album, name='delete_album'),
    path('<album_slug>/delete/song/<song_slug>/', delete_song, name='delete_song'),
    path('search/', search, name='search'),
    path('<album_slug>/favourite_album/', favourite_album, name='favourite_album'),
    path('<album_slug>/<song_slug>/favourite_song/', favourite_song, name='favourite_song'),
    path('favourite_songs/', favourite_songs, name='favourite_songs'),
    path('favourite_albums/', favourite_albums, name='favourite_albums'),
]
