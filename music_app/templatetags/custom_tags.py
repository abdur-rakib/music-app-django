from django import template
register = template.Library()

from ..models import FavouriteAlbum, FavouriteSong

@register.simple_tag
def is_favourite_album(user, album):
    return FavouriteAlbum.objects.filter(user=user, album=album).exists()

@register.simple_tag
def is_favourite_song(user, song):
    return FavouriteSong.objects.filter(user=user, song=song).exists()
