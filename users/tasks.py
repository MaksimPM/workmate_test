import random
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from users.models import User
from django.core.mail import send_mail


@shared_task
def send_confirmation_email(user_id):
    user = User.objects.get(id=user_id)
    confirmation_code = str(random.randint(100000, 999999)).zfill(6)

    user.confirmation_code = confirmation_code
    user.confirmation_code_created_at = timezone.now()
    user.save()

    subject = 'Добро пожаловать!'
    message = (f'Привет!\n'
               f'Добро пожаловать на платформу\n'
               f'Ваш код для подтверждения почты:\n {confirmation_code}')
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)


@shared_task
def send_password_reset_email(user_id):
    user = User.objects.get(id=user_id)
    print(f'Письмо для сброса пароля отправлено - {user.email}')
    subject = 'Cброс пароля'
    message = f'Перейдите по ссылке для сброса пароля: http://127.0.0.1:8000/users/recovery/{user.password}/'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
