from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.models import BorrowRequest
from inventory.models import Product


class InitiateBorrowRequestView(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = BorrowRequest
    fields = ("quantity", "start_date", "end_date", "reason")
    permission_required = ("core.add_request",)
    template_name = "core/borrow_request/add.html"
    extra_context = {"title": "Initiate Borrow Request"}
    success_url = reverse_lazy("core:available_products_list")

    def get_success_message(self, *args, **kwargs):
        return f"You have successfuly request {self.object.quantity} {self.object.product} {self.object.product.measurment}."

    def form_valid(self, form):
        if self.is_quantify_valid(form) and self.is_dates_valid(form):
            form.instance.product = self.product
            form.instance.user = self.request.user
            return super().form_valid(form)
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
        form["quantity"].field.widget.attrs["max"] = self.availables
        return form

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.product = get_object_or_404(Product, slug=self.kwargs["slug"])
        self.availables = self.product.availables

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'previous_borrow_requests': BorrowRequest.objects.filter(
                product=self.product,
                status=0
            ).order_by('date_requested').values('start_date', 'end_date', 'quantity')
        })
        return context_data