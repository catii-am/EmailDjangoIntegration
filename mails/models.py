from django.db import models


class EmailAccount(models.Model):
    provider_choices = [
        ('yandex', 'Yandex'),
        ('gmail', 'Gmail'),
        ('mailru', 'Mail.ru')
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    provider = models.CharField(max_length=20, choices=provider_choices)

    def __str__(self):
        return self.email


class EmailMessage(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField(default=list)

    def __str__(self):
        return self.subject
