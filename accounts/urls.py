from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('update/profile/', profile_update, name='profile_update')
]
