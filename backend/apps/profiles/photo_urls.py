from django.urls import path

from .views import (
    ProfilePhotoDetailView,
    ProfilePhotoUploadView,
    SetPrimaryProfilePhotoView,
)


urlpatterns = [
    path("upload/", ProfilePhotoUploadView.as_view()),
    path("<uuid:pk>/set-primary/", SetPrimaryProfilePhotoView.as_view()),
    path("<uuid:pk>/", ProfilePhotoDetailView.as_view()),
]
