from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from django_summernote.fields import SummernoteTextFormField

import astu_inventory.apps.core.signals as signals
from astu_inventory.apps.core.forms import ReasonForm
from astu_inventory.apps.core.models import BorrowRequest
from astu_inventory.apps.inventory.models import Product


class InitiateBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = BorrowRequest
    fields = ("quantity", "start_date", "end_date", "reason")
    permission_required = "core.can_initiate_borrow_request"
    template_name = "core/borrow_request/add.html"
    extra_context = {"title": "Initiate Borrow Request"}
    success_url = reverse_lazy("core:dashboard")

    def get_success_message(self, *args, **kwargs):
        return (
            f"You have successfuly request {self.object.quantity}"
            f" {self.object.product.measurment} of {self.object.product}."
        )

    def form_valid(self, form):
        if self.is_quantify_valid(form) and self.is_dates_valid(form):
            form.instance.product = self.product
            form.instance.user = self.request.user
            response = super().form_valid(form)
            signals.borrow_request_initialized.send(sender=self.model, instance=self.object)
            return response
        return super().form_invalid(form)

    def is_dates_valid(self, form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        if end_date < start_date:
            form.add_error("end_date", "End date must be after start date.")
            return False
        return True

    def is_quantify_valid(self, form):
        quantity = form.cleaned_data["quantity"]
        if quantity > self.availables:
            form.add_error(
                "quantity",
                f"There is only {self.availables} items, please consider lowering your quantity.",
            )
            return False
        return True

    def get_initial(self):
        return {"quantity": self.availables}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["reason"].field = SummernoteTextFormField()
        form["quantity"].field.widget.attrs.update({"max": self.availables, "min": 0})
        return form

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.product = get_object_or_404(Product, slug=self.kwargs["slug"])
        self.availables = self.product.items.aggregate(total=Coalesce(Sum("quantity"), 0))["total"]

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "previous_borrow_requests": BorrowRequest.objects.filter(product=self.product, status=0)
                .order_by("date_requested")
                .values("start_date", "end_date", "quantity")
            }
        )
        return context_data


class ListActiveBorrowRequestView(PermissionRequiredMixin, ListView):
    model = BorrowRequest
    permission_required = "core.can_list_active_borrow_request"
    context_object_name = "borrow_requests"
    extra_context = {"title": "Active Borrow Requests List"}
    template_name = "core/borrow_request/active/list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=0) | Q(status=4))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(
            Q(user__department=user.department)
            | (~Q(user__department=user.department) & Q(product__department=user.department) & Q(status=4))
        )


class ActiveBorrowRequestDetailView(PermissionRequiredMixin, DetailView):
    model = BorrowRequest
    context_object_name = "borrow_request"
    template_name = "core/borrow_request/active/detail.html"
    permission_required = "core.can_view_active_borrow_request"
    extra_context = {"title": "Active Borrow Request "}

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=0) | Q(status=4))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)


class ApproveBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BorrowRequest
    fields = ("status",)
    permission_required = "auser.can_approve_borrow_request"
    success_message = "Borrow request has been approved successfully."
    http_method_names = ["post"]
    success_url = reverse_lazy("core:active_borrow_requests_list")

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=0) | Q(status=4))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)

    def has_next_process(self):
        if self.object.status == 4 or self.object.product.department == self.object.user.department:
            return False
        return True

    def is_quantify_valid(self, quantity, availables):
        if quantity > availables:
            return False
        return True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.is_quantify_valid(self.object.quantity, self.object.product.availables):
            response = super().form_valid(form)
            signals.borrow_request_approved.send(sender=self.model, instance=self.object)
            return response
        messages.error(
            self.request,
            "This request cann't be approved, since currently there is no enough quantity item available.",
        )
        return HttpResponseRedirect(reverse_lazy("core:active_borrow_requests_detail", args=[self.object.pk]))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        new_status = 4 if self.has_next_process() else 1
        form_data.update({"status": new_status})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeclineBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BorrowRequest
    fields = ("status",)
    permission_required = "auser.can_declined_borrow_request"
    success_message = "Borrow request has been declined."
    http_method_names = ["post"]
    success_url = reverse_lazy("core:active_borrow_requests_list")

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=0) | Q(status=4))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)

    def form_valid(self, form):
        reason = self.request.POST.get("reason")
        reason_form = ReasonForm(data={"description": reason})
        if reason_form.is_valid():
            response = super().form_valid(form)
            reason_obj = reason_form.save(commit=False)
            reason_obj.borrow_request = self.object
            reason_obj.save()
            signals.borrow_request_declined.send(sender=self.model, instance=self.object)
            return response
        messages.error(
            self.request,
            "You have to give a reason before declining a request. Please try again.",
        )
        return HttpResponseRedirect(reverse_lazy("core:active_borrow_requests_detail", args=[self.object.pk]))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 2})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class ListApprovedBorrowRequestView(PermissionRequiredMixin, ListView):
    model = BorrowRequest
    permission_required = "core.can_list_approved_borrow_request"
    context_object_name = "borrow_requests"
    extra_context = {"title": "Approved Borrow Requests List"}
    template_name = "core/borrow_request/approved/list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=1))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)


class ApprovedBorrowRequestDetailView(PermissionRequiredMixin, DetailView):
    model = BorrowRequest
    context_object_name = "borrow_request"
    template_name = "core/borrow_request/approved/detail.html"
    permission_required = "core.can_view_approved_borrow_request"
    extra_context = {"title": "Borrow Request "}

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=1))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)


class CompleteBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BorrowRequest
    fields = ("status",)
    permission_required = "auser.can_complete_borrow_request"
    success_message = "Borrow request has been completed successfully."
    http_method_names = ["post"]
    success_url = reverse_lazy("core:approved_borrow_requests_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.borrow_request_completed.send(sender=self.model, instance=self.object)
        return response

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=1))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 6})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class RevokeBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BorrowRequest
    fields = ("status",)
    permission_required = "auser.can_revoke_borrow_request"
    success_message = "Borrow request has been revoked."
    http_method_names = ["post"]
    success_url = reverse_lazy("core:approved_borrow_requests_list")

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=1))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)

    def form_valid(self, form):
        reason = self.request.POST.get("reason")
        reason_form = ReasonForm(data={"description": reason})
        if reason_form.is_valid():
            response = super().form_valid(form)
            reason_obj = reason_form.save(commit=False)
            reason_obj.borrow_request = self.object
            reason_obj.save()
            signals.borrow_request_revoked.send(sender=self.model, instance=self.object)
            return response
        messages.error(
            self.request,
            "You have to give a reason before revoking a request. Please try again.",
        )
        return HttpResponseRedirect(reverse_lazy("core:approved_borrow_requests_detail", args=[self.object.pk]))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 5})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class ListCompletedBorrowRequestView(PermissionRequiredMixin, ListView):
    model = BorrowRequest
    permission_required = "core.can_list_completed_borrow_request"
    context_object_name = "borrow_requests"
    extra_context = {"title": "Completed Borrow Requests List"}
    template_name = "core/borrow_request/completed/list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=6))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)


class CompletedBorrowRequestDetailView(PermissionRequiredMixin, DetailView):
    model = BorrowRequest
    context_object_name = "borrow_request"
    template_name = "core/borrow_request/completed/detail.html"
    permission_required = "core.can_view_completed_borrow_request"
    extra_context = {"title": "Completed Borrow Request "}

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=6))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)


class ReturnedBorrowRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BorrowRequest
    fields = ("status",)
    permission_required = "auser.can_return_borrow_request"
    success_message = "Borrowed product has been returned successfully."
    http_method_names = ["post"]
    success_url = reverse_lazy("core:completed_borrow_requests_list")

    def get_queryset(self):
        qs = super().get_queryset().filter(Q(status=6))
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(product__department=user.department)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 7})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.borrow_request_returned.send(sender=self.model, instance=self.object)
        return response


class ListBorrowRequestHistoryView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    model = BorrowRequest
    permission_required = "core.can_list_borrow_request_history"
    context_object_name = "borrow_requests"
    extra_context = {"title": "Borrow Requests History List"}
    template_name = "core/borrow_request/history_list.html"

    def get_queryset(self):
        current_user = self.request.user
        return (
            super()
            .get_queryset()
            .filter(user=current_user)
            .values("product__name", "quantity", "start_date", "end_date", "status")
        )
