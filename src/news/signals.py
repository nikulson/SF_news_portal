from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Post
from .views import send_mail_for_subscribers


@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, **kwargs):
    print('Сигнал - начало')
    send_mail_for_subscribers(instance)
    print('Сигнал - конец')
