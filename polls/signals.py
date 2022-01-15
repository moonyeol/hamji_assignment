import datetime

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from polls.models import Choice, Question


@receiver(pre_save, sender=Choice)
def save_choice(sender, instance, **kwargs):
    if not instance.pk:
        if instance.question.choice_set.count() >= 10:
            raise ValueError("You can only suggest Less than 10 choices.")


@receiver(post_save, sender=Choice)
def extend_closed(sender, instance, **kwargs):
    if instance.question.closed_at:
        instance.question.closed_at += datetime.timedelta(days=1)
        instance.question.save()
