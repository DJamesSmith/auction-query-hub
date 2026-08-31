from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def log_user_status_change(sender, instance, **kwargs):
    # Optional: Log when a user's status changes. You can remove this if you don't need logging.
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            if old_user.status != instance.status:
                status_text = "activated" if instance.status else "soft-deleted"
                print(f"User {instance.username} (ID: {instance.id}) has been {status_text}")
        except User.DoesNotExist:
            pass