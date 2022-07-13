from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader


def send_notification(recipients, subject, template, **kwargs):
    sender = settings.SERVER_EMAIL
    template = loader.get_template(template)
    email = EmailMessage(
        subject,
        template.render(kwargs),
        sender,
        recipients,
    )
    email.send()
