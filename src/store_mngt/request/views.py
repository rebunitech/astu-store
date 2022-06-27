from dataclasses import fields
from distutils import dep_util
import urllib.request
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from auser.models import Staffmember
from django.conf import settings
from .forms import *
from .models import Item, Request 
from datetime import datetime
User = settings.AUTH_USER_MODEL





class AddRequestView(CreateView):
    model = Request
    fields = (
        "item",
        "quantity",
        "start_date",
        "end_date",
        "category",
        
    )

    template_name = "request/send_create.html"
    success_url = reverse_lazy("request:request_list")
    permission_required = ("request.can_add_request",)
    success_message = "request added successfully"    


    
    def form_valid(self, form):
        form.instance.department = self.request.user.staffmember.department
        return super().form_valid(form)
   
class RequestListView(ListView):
    model = Request
    template_name = "request/request_list.html"
    permission_required = ("request.can_view_request_list",)
    extra_context = {"title": _("Request List")}
    context_object_name = "requests"
    paginate_by: int = 10

    def get_queryset(self):
        return self.model.objects.filter(department=self.request.user.staffmember.department, is_approved=None , is_requesting = True)

class ListItemView(ListView):
    model = Item
    template_name = "item/item_list.html"
    permission_required = ("request.view_item",)

    context_object_name = "items"
    paginate_by: int = 10       


class AddItemView(CreateView):
    model = Item   
    fields = "__all__"
    template_name = "request/add_item.html"
    success_url = reverse_lazy("request:add_item")
    extra_context = {"title": ("Add Item")}
    success_message = "item added successfully"

class ItemUpdateView(UpdateView):
    model = Item
    fields = "__all__"
    template_name = "request/send_create.html"
    success_url = reverse_lazy("item_list")

class DeleteRequestView(DeleteView):
    model = Request

    template_name: str = "request/delete_request.html"
    success_url = reverse_lazy("request:request_list")
    permission_required = ("request.can_delete_request",)
    success_message = "Request successfully deleted"
    extra_context = {"title": _("Store Keeper Detail")}


class RequestDetailView(DetailView,SuccessMessageMixin,PermissionRequiredMixin):
    model = Request
    template_name = "request/request_detail.html"
    permission_required = ("request.can_view_request_detail",)
    context_object_name = "request"
    extra_context = {"title": _("Request Detail")}
# added request history detail for the requester also!! 
class RequestHistoryView(DetailView,SuccessMessageMixin, PermissionRequiredMixin):
    model = Request
    template_name = "request/request_historyy.html"
    permission_required = ("request.can_view_request_history",)  
    context_object_name = "requests"
    extra_context = {"title": _("Your Request History ")}
    


class ApproveUserRequest(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to approve request"""

    model = Request
    fields = ("is_approved",)
    permission_required = ("request.can_approve_request",)
    success_url = reverse_lazy("request:approved_list")
    success_message = " approved successfully"
    http_method_names = ["post"]


    def form_valid(self, form):
        form.instance.is_approved = True
        self.object.item.quantity -= self.object.quantity
        self.object.item.save()
        response = super().form_valid(form)
        if self.object.department != self.object.item.department:
            Request.objects.create(
                item=self.object.item,
                department=self.object.item.department,
                quantity=self.object.quantity,
                start_date=self.object.start_date,
                end_date=self.object.end_date,
                category=self.object.category,
            )
            
        return response

class ListApprovedRequestView(PermissionRequiredMixin, ListView):
    """Generic view used to list all approved requests"""

    model = Request
    template_name = "request/list_approved.html"
    permission_required = ("request.can_view_request_approve",)
    extra_context = {"title": ("Approved Requests")}
    context_object_name = "requests"

    def get_queryset(self):
        return self.model.objects.filter(is_approved=True, is_given='')

class DeclineUserRequest(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to decline request"""

    model = Request
    fields = ("is_approved",)
    permission_required = ("request.can_decline_request",)
    success_url = reverse_lazy("request:declined_list")
    success_message = "declined request successfully"
    http_method_names = ["post"]
    
    def form_valid(self, form):
        form.instance.is_approved = False
        return super().form_valid(form)

class ListDeclinedRequestView(PermissionRequiredMixin, ListView):
    """Generic view used to list all declined requests"""

    model = Request
    template_name = "request/list_declined.html"
    permission_required = ("request.can_view_request_decline",)
    extra_context = {"title": ("declined requests")}
    context_object_name = "requests"

    def get_queryset(self):
        return self.model.objects.filter(is_approved=False)        

    
class DetailItemView(DetailView):

    model = Item
    template_name: str= "item/item_detail.html"
    extra_context = {"title": ("Item detail")}
    context_object_name = "item"

class CompleteUserRequest(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to complete request"""

    model = Request
    fields = ("is_given",)
    permission_required = ("request.can_complete_request",)
    success_url = reverse_lazy("request:borrowed_list")
    success_message = " completed  successfully"
    http_method_names = ["post"]
            
    def form_valid(self, form):
        form.instance.is_given = True
        return super().form_valid(form)
    def get_queryset(self):
        return self.model.objects.filter(is_given=False) 
    def get_queryset(self):
        return self.model.objects.filter(is_given=None)     

class ListCompletedUserRequest(PermissionRequiredMixin, ListView):
    """Generic view used to list all borrowed  requests"""

    model = Request
    template_name = "request/list_completed.html"
    permission_required = ("request.can_view_request_complete",)
    extra_context = {"title": ("borrowed items list:")}
    context_object_name = "requests"

    def get_queryset(self):
        return self.model.objects.filter(is_given=True)    
class ReturnRequestedItem(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to complete request"""

    model = Request
    fields = ("is_returned",)
    permission_required = ("request.can_return_request",)
    success_url = reverse_lazy("request:returned_list")
    success_message = " returned successfully"
    http_method_names = ["post"]

    def form_valid(self, form):
        form.instance.is_returned = True
        return super().form_valid(form)
    

    def get_queryset(self):
         return self.model.objects.filter(is_returned=False) 
    def get_queryset(self):
         return self.model.objects.filter(is_returned=None)  
     

class ListReturnedUserRequest(PermissionRequiredMixin, ListView):
    """Generic view used to list all returned  request items"""

    model = Request
    template_name = "request/list_returned.html"
    permission_required = ("request.can_view_request_return",)
    extra_context = {"title": ("returned requests")}
    context_object_name = "requests"

    def get_queryset(self):
        return self.model.objects.filter(is_returned=True)  
class BorrowDetailView(DetailView,PermissionRequiredMixin,SuccessMessageMixin):
    model = Request
    template_name = "request/borrow_detail.html"
    permission_required = ("request.can_view_request_detail",)
    context_object_name = "request"
    extra_context = {"title": _("Borrow Detail")}  

class CancelRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to cancel request"""

    model = Request
    fields = ("is_requesting",)
    permission_required = ("request.can_cancel_request",)
    success_url = reverse_lazy("request:add_request")
    success_message = " cancelled successfully"
    http_method_names = ["post"]

    def form_valid(self, form):
        form.instance.is_requesting = False
        return super().form_valid(form)
    def get_queryset(self):
         return self.model.objects.filter(is_requesting=True)     
    