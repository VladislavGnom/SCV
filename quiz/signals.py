from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestAttempt

@receiver(post_save, sender=TestAttempt)
def update_user_stats(sender, instance, created, **kwargs):
    if created and instance.completed_at:
        profile = instance.user.profile
        profile.tests_taken += 1
        profile.save()