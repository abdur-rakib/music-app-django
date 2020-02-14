from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django .contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import *
from .forms import *

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']


class AlbumView(ListView):
    model = Album
    template_name = 'music/album.html'
    queryset = Album.objects.filter(private=False)
    context_object_name = 'albums'
    paginate_by = 8

    extra_context = {
        'title': 'Album',
        'album_page': 'active'
    }


class AlbumCreateView(LoginRequiredMixin, CreateView):
    template_name = 'music/album_create.html'
    form_class = AlbumCreateForm
    extra_context = {
        'title': "Add a new album",
        'create_page': 'active'
    }

    def get_success_url(self):
        return reverse('music:album_detail', args=(self.object.slug,))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        self.object.save()
        messages.success(self.request, 'Album added successfully')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(self.get_success_url()))


class SongCreateView(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': SongCreateForm()}
        return render(request, 'music/song_create.html', context)

    def post(self, request, slug, *args, **kwargs):
        album = get_object_or_404(Album, slug=slug)
        form = SongCreateForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = self.request.user
            song.album = album

            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/song_create.html', context)

            song.save()
            messages.success(
                self.request, f"'{song.song_title}' added successfully")
            return HttpResponseRedirect(reverse_lazy('music:album_detail', args=[song.album.slug]))
        return render(request, 'music/song_create.html', {'form': form})


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'


def delete_album(request, slug):
    album = get_object_or_404(Album, slug=slug)
    if request.method == "POST":
        album.delete()
        messages.warning(request, 'Album deleted successfully')
        return HttpResponseRedirect(reverse_lazy('music:album'))
    context = {
        'album': album
    }
    return render(request, 'music/album_delete.html', context)


def delete_song(request, album_slug, song_slug):
    song = get_object_or_404(Song, slug=song_slug)
    album = get_object_or_404(Album, slug=album_slug)

    if request.method == "POST":
        song.delete()
        messages.warning(request, 'Song deleted successfully')
        return HttpResponseRedirect(reverse_lazy('music:album_detail', args=[album_slug]))
    context = {
        'song': song,
        'album': album
    }
    return render(request, 'music/song_delete.html', context)


def search(request):
    query = request.GET.get('q')

    if query:
        albums = Album.objects.filter(
            Q(album_title__icontains=query)
        )
        songs = Song.objects.filter(
            Q(song_title__icontains=query)
        )

    context = {
        'albums': albums,
        'songs': songs,
        'query': query
    }
    return render(request, 'search_results.html', context)


def favourite_album(request, album_slug):
    album = get_object_or_404(Album, slug=album_slug)

    fav_album, created = FavouriteAlbum.objects.get_or_create(
        user=request.user, album=album)

    if created:
        messages.success(request, 'Album added to favourite!!!')
    else:
        fav_album.delete()

        messages.warning(request, 'Album removed from favourite!!!')

    return HttpResponseRedirect(reverse_lazy('music:album_detail', args=[album_slug]))


def favourite_song(request, album_slug, song_slug):
    # album = get_object_or_404(Album, slug=album_slug)
    song = get_object_or_404(Song, slug=song_slug)

    fav_song, created = FavouriteSong.objects.get_or_create(
        user=request.user, song=song)

    if created:
        messages.success(request, 'Song added to favourite!!!')
    else:
        fav_song.delete()
        messages.warning(request, 'Song removed from favourite!!!')

    return HttpResponseRedirect(reverse_lazy('music:album_detail', args=[album_slug]))


@login_required
def favourite_songs(request):
    songs = FavouriteSong.objects.filter(user=request.user)
    context = {
        'songs': songs,
        'songs_page': 'active'
    }
    return render(request, 'music/favourite_songs.html', context)


@login_required
def favourite_albums(request):
    albums = FavouriteAlbum.objects.filter(user=request.user)
    context = {
        'albums': albums,
        'songs_page': 'active'
    }
    return render(request, 'music/favourite_albums.html', context)
