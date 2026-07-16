import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from apps.profiles.models import Profile, ProfilePhoto
from apps.users.models import User


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProfilePhotoAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            phone="9999999999",
            password="password",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            phone="8888888888",
            password="password",
        )
        self.profile = self.create_profile(self.user, "Owner Profile")
        self.other_profile = self.create_profile(self.other_user, "Other Profile")
        self.client.force_authenticate(self.user)

    def create_profile(self, user, full_name):
        return Profile.objects.create(
            user=user,
            full_name=full_name,
            gender="male",
            date_of_birth="1995-01-01",
            marital_status="never_married",
            children_status="none",
            religion="Hindu",
            mother_tongue="Hindi",
            height_cm=175,
            education="Graduate",
            occupation="Engineer",
            country="India",
            state="Delhi",
            city="Delhi",
        )

    def image_file(self, name="photo.gif"):
        return SimpleUploadedFile(
            name,
            (
                b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,"
                b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )

    def test_upload_lists_and_sets_first_photo_primary(self):
        response = self.client.post(
            "/api/photos/upload/",
            {"profile": self.profile.id, "image": self.image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        photo = ProfilePhoto.objects.get(profile=self.profile)
        self.assertTrue(photo.is_primary)

        response = self.client.get(f"/api/photos/{self.profile.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(photo.id))

    def test_cannot_upload_photo_for_another_users_profile(self):
        response = self.client.post(
            "/api/photos/upload/",
            {"profile": self.other_profile.id, "image": self.image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            ProfilePhoto.objects.filter(profile=self.other_profile).exists()
        )

    def test_set_primary_photo_clears_existing_primary_for_profile(self):
        primary = ProfilePhoto.objects.create(
            profile=self.profile,
            image=self.image_file("primary.gif"),
            is_primary=True,
        )
        secondary = ProfilePhoto.objects.create(
            profile=self.profile,
            image=self.image_file("secondary.gif"),
        )

        response = self.client.post(f"/api/photos/{secondary.id}/set-primary/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        primary.refresh_from_db()
        secondary.refresh_from_db()
        self.assertFalse(primary.is_primary)
        self.assertTrue(secondary.is_primary)
        self.assertEqual(
            ProfilePhoto.objects.filter(profile=self.profile, is_primary=True).count(),
            1,
        )

    def test_can_delete_only_own_photo(self):
        own_photo = ProfilePhoto.objects.create(
            profile=self.profile,
            image=self.image_file("own.gif"),
        )
        other_photo = ProfilePhoto.objects.create(
            profile=self.other_profile,
            image=self.image_file("other.gif"),
        )

        response = self.client.delete(f"/api/photos/{other_photo.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(ProfilePhoto.objects.filter(id=other_photo.id).exists())

        response = self.client.delete(f"/api/photos/{own_photo.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProfilePhoto.objects.filter(id=own_photo.id).exists())
