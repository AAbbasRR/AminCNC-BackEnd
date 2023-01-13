from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Picture


@receiver(post_delete, sender=Picture)
def delete_picture_file_handler(sender, instance, **kwargs):
    instance.picture.delete(False)
