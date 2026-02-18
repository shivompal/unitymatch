from django.urls import path
from .views import (
    CreateProfileView,
    MyProfilesView,
    UpdateProfileView,
    DeleteProfileView,
)

urlpatterns = [
    path("", CreateProfileView.as_view()),
    path("me/", MyProfilesView.as_view()),
    path("<uuid:pk>/", UpdateProfileView.as_view()),
    path("<uuid:pk>/delete/", DeleteProfileView.as_view()),
]
