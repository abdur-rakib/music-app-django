from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .forms import ProfileUpdateForm

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'profile'


@login_required(login_url='account_login')
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile has been updated!')
            return HttpResponseRedirect(reverse('profile', args=[request.user.id]))

    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'profile/edit_profile.html', context)
