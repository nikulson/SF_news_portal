from datetime import timedelta

from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.utils.datetime_safe import date

from .models import Post, Category
from .views import send_mail_for_sub
from ..config import settings


@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Dear {email_address.user} Welcome to my News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='FPW-13@yandex.ru',
        recipient_list=[email_address.user.email]
    )


@receiver(m2m_changed, sender=Post.category.through)
def new_post(sender, action, instance, **kwargs):
    if action == 'post_add':
        for each in instance.category.all():
            for cat in each.subscribers.all():
                send_mail(
                    subject=f'A new post named "{instance.title}" is created!',
                    message=f'{instance.created_at.strftime("%d %m %Y")} - {instance.content[:10]}',
                    from_email='nikulshinsf@yandex.ru',
                    recipient_list=[cat.email]
                )

                print(cat.email)


@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):
    print('Сигнал - начало')
    send_mail_for_sub(instance)
    print('Сигнал - конец')


def week_post_2():
    if date.today().weekday() == 1:  # если сегодня понедельник
        start = date.today() - timedelta(7)  # Вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки
        # дат
        finish = date.today()  # сегодняшний день - конец диапазона выборки дат

        # список постов, отфильтрованный по дате создания в диапазоне start и finish
        list_of_posts = Post.objects.filter(date_created__range=(start, finish))

        # все возможные категории
        categories = Category.objects.all()

        # возьмём все возможные категории и пробежимся по ним
        for category in categories:
            # создадим список, куда будем собирать почтовые адреса подписчиков
            subscribers_emails = []
            # из списка всех пользователей
            for user in User.objects.all():
                # отфильтруем только тех, кто подписан на конкретную категорию, по которой идёт выборка
                # делаем это за счёт того, что в модели Category в поле subscribers
                # мы добавили имя обратной связи от User к Category, чтобы получить доступ
                # ко всем связанным объектам пользователя --> related_name='subscriber'
                user.subscriber.filter(article_category=category)
                # добавляем в список адреса пользователей, подписанных на текущую категорию
                subscribers_emails.append(user.email)

                # укажем контекст в виде словаря, который будет рендерится в шаблоне week_posts.html
                html_content = render_to_string('news_list/week_posts.html',
                                                {'posts': list_of_posts, 'category': category})

                # формируем тело письма
                msg = EmailMultiAlternatives(
                    subject=f'Все новости за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()  # отсылаем
