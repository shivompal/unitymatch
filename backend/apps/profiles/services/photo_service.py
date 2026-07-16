from django.db import transaction

from apps.profiles.models import ProfilePhoto


@transaction.atomic
def set_primary_photo(photo):
    ProfilePhoto.objects.select_for_update().filter(profile=photo.profile).update(
        is_primary=False
    )
    photo.is_primary = True
    photo.save(update_fields=["is_primary"])
    return photo
