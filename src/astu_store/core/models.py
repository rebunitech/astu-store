from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.validators import validate_past
from inventory.models import Item, Product

UserModel = get_user_model()


class BorrowRequest(models.Model):
    class StatusChoice(models.IntegerChoices):
        PENDING = 0, "Pending"  # request does not get any reponse
        APPROVED = 1, "Approved"  # request has been approved by representative
        DECLINED = 2, "Declined"  # request has been declined by representative
        CANCELLED = (
            3,
            "Cancelled",
        )  # request has been cancelled by the requestor (staff)
        PROCESSING = (
            4,
            "Processing",
        )  # request has been transfered for futher verification
        REVOKED = 5, "Revoked"  # request has been denined by store/lab officer
        PROCESSED = (
            6,
            "Processed",
        )  # request has been completed. item is given to requester

    product = models.ForeignKey(
        Product,
        verbose_name="product",
        related_name="borrow_requests",
        on_delete=models.PROTECT,
    )
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateTimeField("start date", validators=[validate_past])
    end_date = models.DateTimeField("end date", validators=[validate_past])
    user = models.ForeignKey(
        UserModel,
        verbose_name="user/requester",
        related_name="borrow_requests",
        on_delete=models.SET_NULL,
        null=True,
    )
    reason = models.TextField("reason")
    status = models.IntegerField(
        choices=StatusChoice.choices, default=StatusChoice.PENDING
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrow_request"
        verbose_name = "borrow request"
        verbose_name_plural = "borrow requests"


class Reason(models.Model):
    request = models.OneToOneField(
        BorrowRequest,
        verbose_name="request",
        related_name="response_reason",
        on_delete=models.CASCADE,
    )
    description = models.TextField("description")

    class Meta:
        db_table = "reason"
        verbose_name = "reason"
        verbose_name_plural = "reasons"


class BorrowHistory(models.Model):
    borrow_request = models.ForeignKey(
        BorrowRequest,
        verbose_name="borrow requests",
        related_name="histories",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item, verbose_name="item", related_name="items", on_delete=models.CASCADE
    )
    quantity = models.SmallIntegerField("quantity")

    class Meta:
        db_table = "borrow_history"
        verbose_name = "borrow history"
        verbose_name_plural = "borrow histories"