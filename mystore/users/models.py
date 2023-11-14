from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Action Required: Verify Your Registration for "{self.user.username}" to Activate Your Account'
        message = (
            f"Hello {self.user.username},\n\n"
            f"Welcome to Fun Store! We're excited to have you on board. To get started, we need to verify your email "
            f"address. This is a quick step to ensure the security of your account and to provide you with a seamless "
            f"experience.\n\n"
            f"Please click the link below to verify your email address:\n"
            f"{verification_link}\n\n"
            f"This link will be active for 48 hours. If you did not create an account with us, please ignore this "
            f"email.\n\n"
            f"Thank you for joining us at 🛒 Fun Store! If you have any questions or need assistance, feel free to "
            f"reach out to our support team.\n\n"
            f"Best regards,\n"
            f"Team 🛒 Fun Store "
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
