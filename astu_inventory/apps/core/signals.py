from django.dispatch import Signal, receiver

from astu_inventory.apps.core.models import BorrowRequest
from astu_inventory.apps.core.utils import send_notification

borrow_request_initialized = Signal()
borrow_request_approved = Signal()
borrow_request_declined = Signal()
borrow_request_cancelled = Signal()
borrow_request_proccessed = Signal()
borrow_request_revoked = Signal()
borrow_request_completed = Signal()
borrow_request_returned = Signal()


@receiver(borrow_request_initialized, sender=BorrowRequest)
def initialized(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "You initialized borrow request."
    template_name = "emails_responses/initialized.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_approved, sender=BorrowRequest)
def approved(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "Approval of your borrow request."
    template_name = "email_responses/approved.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_declined, sender=BorrowRequest)
def declined(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "Your request has been declined."
    template_name = "email_responses/declined.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_proccessed, sender=BorrowRequest)
def proccessed(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "Your request is directed to the department."
    template_name = "email_responses/proccessed.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_completed, sender=BorrowRequest)
def completed(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "Your borrow request is completed."
    template_name = "email_responses/completed.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_revoked, sender=BorrowRequest)
def revekod(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "Your borrow request is REVOKED."
    template_name = "email_responses/revoked.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})


@receiver(borrow_request_returned, sender=BorrowRequest)
def returned(sender, instance=None, **kwargs):
    recipients = (instance.user.email,)
    subject = "You returned the item to the store."
    template_name = "emails_responses/returned.txt"
    send_notification(recipients, subject, template_name, **{"borrow_request": instance})
