from django import forms
from .models import *




class AlbumCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlbumCreateForm, self).__init__(*args, **kwargs)
        self.fields['private'].label = 'Private'

    artist = forms.CharField(label='Artist name',widget=forms.TextInput(attrs={'placeholder':'Artist', 'class': 'form-control'}))
    album_title = forms.CharField(label='Album title',widget=forms.TextInput(attrs={'placeholder':'Album title', 'class': 'form-control'}))
    album_logo = forms.FileField(label='Album logo',widget=forms.FileInput(attrs={
        'placeholder':'Album logo',
        'type': 'file',
        'class': 'file-upload'
        }))

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'album_logo', 'private', ]

    
    def clean_album_title(self):
        album_title = self.cleaned_data['album_title']

        if Album.objects.filter(album_title=album_title).exists():
            raise forms.ValidationError("You have already added a album with same title.")
        return album_title


class SongCreateForm(forms.ModelForm):

    song_title = forms.CharField(label='Album title',widget=forms.TextInput(attrs={'placeholder':'Song title', 'class': 'form-control'}))
    audio_file = forms.FileField(widget=forms.FileInput(attrs={
        'type': 'file',
        'class': 'file-upload'
        }))

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file', ]


    
