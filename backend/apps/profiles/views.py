from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, ProfilePhoto
from .serializers import (
    ProfilePhotoListSerializer,
    ProfilePhotoUploadSerializer,
    ProfileSerializer,
)
from .services.photo_service import set_primary_photo


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyProfilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(user=request.user)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class DeleteProfileView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ProfilePhotoUploadView(generics.CreateAPIView):
    serializer_class = ProfilePhotoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        should_set_primary = serializer.validated_data.get("is_primary", False)
        profile = serializer.validated_data["profile"]
        is_first_photo = not profile.photos.exists()

        photo = serializer.save(is_primary=False)
        if should_set_primary or is_first_photo:
            set_primary_photo(photo)


class ProfilePhotoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk, user=request.user)
        photos = profile.photos.all().order_by("-is_primary", "-created_at")
        serializer = ProfilePhotoListSerializer(
            photos, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        photo = get_object_or_404(
            ProfilePhoto.objects.select_related("profile"),
            pk=pk,
            profile__user=request.user,
        )
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetPrimaryProfilePhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(
            ProfilePhoto.objects.select_related("profile"),
            pk=pk,
            profile__user=request.user,
        )
        set_primary_photo(photo)
        serializer = ProfilePhotoListSerializer(photo, context={"request": request})
        return Response(serializer.data)
