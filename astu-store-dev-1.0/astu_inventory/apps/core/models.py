from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from astu_inventory.apps.core.validators import validate_past
from astu_inventory.apps.inventory.models import Item, Product

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
        COMPLETED = (
            6,
            "Completed",
        )  # request has been completed. item is given to requester
        RETURNED = 7, "Returned"  # borrowed item is returned into store/lab

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
    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.PENDING)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "borrow_request"
        verbose_name = "borrow request"
        verbose_name_plural = "borrow requests"
        permissions = (
            ("can_list_available_product", "Can list available products"),
            ("can_initiate_borrow_request", "Can initiate borrow request"),
            ("can_list_active_borrow_request", "Can list active borrow request"),
            ("can_view_active_borrow_request", "Can view active borrow request"),
            ("can_approve_borrow_request", "Can approve borrow request"),
            ("can_decline_borrow_request", "Can decline borrow request"),
            ("can_list_approved_borrow_request", "Can list approved borrow request"),
            ("can_view_approved_borrow_request", "Can view approved borrow request"),
            ("can_complete_borrow_request", "Can complete borrow request"),
            ("can_revoke_borrow_request", "Can revoke borrow request"),
            ("can_list_completed_borrow_request", "Can list completed borrow request"),
            ("can_view_completed_borrow_request", "Can view completed borrow request"),
            ("can_return_borrow_request", "Can return borrow request"),
            ("can_list_borrow_request_history", "Can list borrow request history"),
        )

    @property
    def leads_under_critical(self):
        return (self.product.availables - self.quantity) <= self.product.critical_no


class Reason(models.Model):
    borrow_request = models.OneToOneField(
        BorrowRequest,
        verbose_name="borrow_request",
        related_name="response_reason",
        on_delete=models.CASCADE,
    )
    description = models.TextField("description")

    class Meta:
        db_table = "reason"
        verbose_name = "reason"
        verbose_name_plural = "reasons"
