from dataclasses import fields
from distutils import dep_util

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
# from auser.models import Staffmember
from django.conf import settings

User = settings.AUTH_USER_MODEL


from .forms import *
from .models import Item, Request 
from datetime import datetime


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

    print(Request.department)
    def form_valid(self, form):
        self.object.department = self.object.item.department
        self.object = form.save()
        self.object.save()
        # print()
        # if item.department == requester.department:
        #     form.instance.is_other_dept = True
        # else:
        #     form.instance.is_other_dept = False    

        return super().form_valid(form)
        
    # def send_new_request(self, user_departemnt):
    #     request = Request(self.department)
   
    # TODO: for other department request

    # def check_dept(self):
    #     item_dept = self.object.item.department
    #     user_dept = self.request.user.staffmember.department

    #     if item_dept == user_dept :
    #         return True
    #     else:
    #         self.send_new_request(user_dept)
        

    # default on model for requesting null
    # x = item department 
    # y = user ( staff member ) department
    # if x = y :
    #     update requesting = True
    # else: 
    #     send_to_user_dept = ......   returned value true(process ) or false(decline)
    #     if  send_to_user_dept:
    #            update value of requesting = true 
    #     if not send_to_dept:
    #         requesting = false
    
    #  $$$ for department to approve (lists of request ) when their requesting attribute become TRUE


     
class RequestListView(ListView):
    model = Request
    template_name = "request/request_list.html"
    permission_required = ("request.view_request",)
    extra_context = {"title": _("Request List")}
    context_object_name = "requests"
    paginate_by: int = 10

    # def get_queryset(self):
    #     return self.model.objects.filter(is_approved = '', is_given='', is_returned='')

# class ListItemView(ListView): #TODO: this is not proper place
#     model = Item
#     template_name = "item/item_list.html"
#     context_object_name = "items"
#     paginate_by: int = 10       


# class AddItemView(CreateView):
#     model = Item   
#     fields = "__all__"
#     template_name = "request/add_item.html"
#     success_url = reverse_lazy("request:add_item")
#     extra_context = {"title": ("Add Item")}
#     success_message = "item added successfully"




# class ItemUpdateView(UpdateView):
#     model = Item
#     fields = "__all__"
#     template_name = "request/send_create.html"
#     success_url = reverse_lazy("item_list")

class DeleteRequestView(DeleteView):
    model = Request

    template_name: str = "request/delete_request.html"
    success_url = reverse_lazy("request:request_list")
    permission_required = ("request.can_delete_request",)
    success_message = "Request successfully deleted"
    extra_context = {"title": _("Store Keeper Detail")}


class RequestDetailView(DetailView):
    model = Request
    template_name = "request/request_detail.html"
    permission_required = ("request.can_view_request_detail",)
    context_object_name = "request"
    extra_context = {"title": _("Request Detail")}



class ApproveUserRequest(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to approve request"""

    model = Request
    fields = ("is_approved",)
    permission_required = ("request.can_approve_request",)
    success_url = reverse_lazy("request:approved_list")
    success_message = " approved successfully"
    http_method_names = ["post"]

    # TODO: check this may be updating is_approve way simple 
    def form_valid(self, form):
        form.instance.is_approved = True
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(is_approved=False)
    def get_queryset(self):
        return self.model.objects.filter(is_approved=None)    
   


class ListApprovedRequestView(PermissionRequiredMixin, ListView):
    """Generic view used to list all approved requests"""

    model = Request
    template_name = "request/list_approved.html"
    permission_required = ("request.can_view_request_approve",)
    extra_context = {"title": ("approved requests")}
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

    def get_queryset(self):
        return self.model.objects.filter(is_approved=True)
    def get_queryset(self):
        return self.model.objects.filter(is_approved=None)    

class ListDeclinedRequestView(PermissionRequiredMixin, ListView):
    """Generic view used to list all declined requests"""

    model = Request
    template_name = "request/list_declined.html"
    permission_required = ("request.can_view_request_decline",)
    extra_context = {"title": ("declined requests")}
    context_object_name = "requests"
    # print([ i for i in context_object_name])

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
    permission_required = ("request.can_view_complete_request",)
    extra_context = {"title": ("Borrowed items list")}
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
    """Generic view used to list all returned  requests"""

    model = Request
    template_name = "request/list_returned.html"
    permission_required = ("request.can_view_return_request",)
    extra_context = {"title": ("returned requests")}
    context_object_name = "requests"

    def get_queryset(self):
        return self.model.objects.filter(is_returned=True)  
class BorrowDetailView(DetailView):
    model = Request
    template_name = "request/borrow_detail.html"
    permission_required = ("request.can_view_request_detail",)
    context_object_name = "request"
    extra_context = {"title": _("Borrow Detail")}  


# for date
# def table_search(request):
#   initial_start = "2015/2"
#   initial_end = "2015/222"
#   message = {'last_url':'table_search'}

#   if request.method == "POST":
#     daterange_form = DateRangeForm(request.POST,required=True,initial_start_date=initial_start,initial_end_date=initial_end)

#   else:
#     daterange_form = DateRangeForm(required=True,initial_start_date=initial_start,initial_end_date=initial_end)
#     search_dict.update({'daterange_form':daterange_form})

#   return render(request, 'InterfaceApp/table_search.html', search_dict)