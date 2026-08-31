from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User
from auctions.models import AuctionItem


@receiver(pre_save, sender=User)
def hide_user_auctions_on_soft_delete(sender, instance, **kwargs):
    # When a user is soft-deleted (status changes from True to False), automatically hide all their auction items.
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            # If user status changed from active to inactive (soft delete)
            if old_user.status is True and instance.status is False:
                # Hide all auctions belonging to this user
                AuctionItem.objects.filter(seller=instance).update(is_active=False)
            # If user status changed from inactive to active (restore)
            elif old_user.status is False and instance.status is True:
                # Show all auctions belonging to this user
                AuctionItem.objects.filter(seller=instance).update(is_active=True)
        except User.DoesNotExist:
            pass