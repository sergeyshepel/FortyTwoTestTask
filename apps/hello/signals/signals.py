from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from hello.models import DBActionsLog


@receiver(post_save)
def object_created_or_updated_signal(sender, created, **kwargs):
    if sender.__name__ != 'DBActionsLog':
        if created:
            DBActionsLog.objects.create(model=sender.__name__,
                                        action='created')
        else:
            DBActionsLog.objects.create(model=sender.__name__,
                                        action='updated')
    return


@receiver(post_delete)
def object_removed_signal(sender, **kwargs):
    if sender.__name__ != 'DBActionsLog':
        DBActionsLog.objects.create(model=sender.__name__,
                                    action='deleted')
    return
