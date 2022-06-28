from gc import get_objects
import urllib.request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView,DetailView
from maintenace.forms import AddMaintenaceRequest
from maintenace.models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class AddMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceRequest
    fields = (
        "item",
        "quantity",    
        "problem",
    )
    permission_required = ("maintenace.add_maintenacerequest",)
    success_message = _('maintenace request added successfully.')
    template_name = "maintenace/add_maintenance_request.html"
    extra_context = {"title": _("Add maintenace requests")}
    
    def get_success_url(self):
        print(self.object)
        return reverse_lazy(
            "maintenace:list_maintenacerequests",
        )

    """list maintenace request view """    

class ListMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin,  ListView):
    model = MaintenanceRequest
    permission_required = ("maintenace.view_maintenancerequest",)
    template_name = "maintenace/list_maintenance_request.html"
    context_object_name = 'maintenance_requests'
    extra_context = {"title": _("List maintenace requests")}
    
    def get_queryset(self):
        return self.model.objects.filter(is_approved=False, is_declined = False, is_request=True)
     
    
""" update maintenace request view """

class UpdateMaintenanceRequestView(UpdateView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = MaintenanceRequest
    fields = (
        "item",
        "quantity",
        "problem",
    )
    permission_required = "maintenace.change_maintenancerequest"
    template_name = "maintenace/update_maintenace_request.html"
    success_message = 'Maintenance request of %(item)s updated successfully.'
    success_url = reverse_lazy("maintenace:list_maintenacerequests")
    context_object_name = "update_maitenance"
    extra_context = {"title": _("Update Maintenance Request")}
    
    
class CancelMaintenaceRequestView(UpdateView, PermissionRequiredMixin, SuccessMessageMixin):
        """ cancel request view """
        model = MaintenanceRequest
        fields = ("is_request",)
        permission_required = "maintenace.cancel_maintenancerequest"
        success_url = reverse_lazy("maintenace:canceled_list")
        success_message = "Maintenace request cancelled successfully"
        http_method_names = ["post"]
        
        def get_form_kwargs(self):
            form_kwargs = super().get_form_kwargs()
            form_data = form_kwargs.get("data", {}).copy()
            form_data.update({ "is_request" : False})
            form_kwargs.update({"data": form_data})
            return form_kwargs

        def get_queryset(self):
            return self.model.objects.filter(is_request=True)
    
class CanceledListMaintenanceRequestView(PermissionRequiredMixin, ListView, SuccessMessageMixin):
    """ Generic view for canceled maintenance request """
    model = MaintenanceRequest
    permission_required = "view_canceled_maintenancerequest"
    template_name = "maintenace/canceled_list_request.html"
    context_object_name = "canceled_request"
    extra_context = {"title": "Canceled Maintenance Request" }
    
    def get_queryset(self):
        return self.model.objects.filter(is_request=False)
    
class ApproveMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
    """Generic view used to approve request (undermaintenace)"""
    
    model =  MaintenanceRequest
    fields = ("is_approved",)
    permission_required = "maintenace.can_approve"
    success_url = reverse_lazy("maintenace:lists_approved_request")
    success_message = "Maintenace request approved successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_approved": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_approved=False)
    
    # def form_valid(self,form):
    #     self.object.item.quantity -= self.object.quantity  #when request approved it subtracts requested item from available
    #     self.object.item.save()
    
"""list of approved (undermaintenace ) request view """

class ListApprovedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
        model =  MaintenanceRequest
        template_name = "maintenace/lists_undermaintenance.html"
        permission_required = "maintenace.view_list_approved_maintenance_request"
        extra_context = {"title": _("Approved Maintenance Request")}
        context_object_name = "list_approved"
        
        def get_queryset(self):
            return self.model.objects.filter(is_approved=True,is_damaged=False,is_repaired =False)
class DeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to declined request"""
    model =  MaintenanceRequest
    fields = ("is_declined",)
    permission_required = "maintenace.can_decline"
    success_url = reverse_lazy("maintenace:lists_declined_request")
    success_message = "Maintenace request declined successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        # description = request.POST.get("reason") "decline_reason": description,
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_declined": True,  })
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_declined=False)
    
"""" list view for declined maintenace request view """

class ListDeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    """Generic view used to declined request list"""
    
    model =  MaintenanceRequest
    template_name = "maintenace/declined_list.html"
    permission_required = "maintenace.view_list_declined_maintenance_request"
    context_object_name = "list_declined"
    extra_context = {"title": _("Declined Maintenance Request")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_declined=True)
        
    """generic view for repaired item list """
    
class RepairedMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
         model =  MaintenanceRequest
         fields = ("is_repaired",)
         permission_required = "maintenace.can_repaire"
         template_name = "maintenace/lists_undermaintenance.html"
         success_url = reverse_lazy("maintenace:list_repaired_request_list")
         success_message = " Items request repaired successfully"
         http_method_names = ["post"]
         
         
        #  def get_context_data(self, **kwargs):
        #      return super().get_context_data(**kwargs)
        
        #  def get_form_kwargs(self):
        #     form_kwargs = super().get_form_kwargs()
        #     form_data = form_kwargs.get("data", {}).copy()
        #     form_data.update({"is_repaired": True})
        #     form_kwargs.update({"data": form_data})
        #     return form_kwargs
        #  def get_item(self):
        #     failurity_report = get_object_or_404(FailurityReport ,pk=self.kwargs['item_pk'] )
        #     return failurity_report.item
        
         def form_valid(self, form):
            form.instance.is_repaired = True
            form.save()
            return super().form_valid(form)
            
        
        
        
        
class ListRepairedMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    model =  MaintenanceRequest
    template_name = "maintenace/list_repaired_maintenace.html"
    permission_required = "maintenace.view_list_repaired_maintenance_request"
    context_object_name = "list_repaired_item"
    extra_context = {"title": _("Repaired Maintenance Request")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_repaired=False)
        
    
""" Add failurity report view  """

class AddFailurityReportView(CreateView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    fields = "__all__"
    permission_required = ("maintenace.add_failurityreport",)
    success_message = _('failurity reports added successfully.')
    template_name = "maintenace/add_failurity_report.html"
    success_url = reverse_lazy("maintenace:list_failurity_report")
    extra_context = {"title": _("Add FailurityReport")}
    

"""" list for failurity report view  """

class ListFailurityReportView(ListView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    permission_required = ("maintenace.view_failurityreport",)
    template_name = "maintenace/list_failurity_report.html"
    context_object_name = "failurity_reports"
    extra_context = {"title": _("list failurity reports")}

"""" detail failurity report view  """

class DetailFailureReprtView(DetailView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    permission_required = ("maintenace.view_failurity_report",)
    template_name = "maintenace/detail_failure_report.html"
    context_object_name = "failurereport"
    extra_context = {"title": _("Detail failurity reports")}
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
        
class AddDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Add damage report from item directly. """
    
    model = DamageReport
    fields = (
        
        "item",
        "quantity",
        "problem",
    )
    permission_required = ("maintenace.add_damagereport",)
    success_message = _('Damage reports added successfully.')
    template_name = "maintenace/add_damage.html"
    success_url = reverse_lazy("maintenace:list_damagereports")
    context_object_name = "add_damage_report"
    extra_context = {"title": _("Add damage reports")}
    

class ListDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    """ Damage Report  list view direct from item. """
    
    model = DamageReport
    permission_required = ("maintenace.view_damagereport",)
    template_name = "maintenace/list_direct_damage.html"
    context_object_name = "damagereports"
    extra_context = {"title": _("list damage reports")}


class AddDamagedMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    
    """ Damaged maintenace report item list from under maintenace (approved item) """
    
    model = DamageReport
    fields = ("is_damaged",)
    permission_required = "maintenace.can_damagemaintenacerequest"
    success_url = reverse_lazy("maintenace:damaged_requests_lists")
    success_message = "Damage report added successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_damaged": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs
    
    def get_item(self):
        # print(self.kwargs)
        failurity_report = get_object_or_404(FailurityReport ,pk=self.kwargs['item_pk'] )
        return failurity_report.item
    
    def form_valid(self, form):
        form.instance.item = self.get_item()
        return super().form_valid(form)
    
    
class ListDamagedMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    model = DamageReport
    template_name = "maintenace/list_damage_maintenance.html"
    permission_required = "maintenace.view_listdamagedmaintenacerequest"
    context_object_name = "list_damaged_maintenace_request"
    extra_context = {"title": _("Damaged Item")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_damaged=True)


