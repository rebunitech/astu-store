from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView,DetailView
from maintenance.forms import AddMaintenanceRequest
from maintenance.models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class AddMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceRequest
    fields = (
        "item",
        "quantity",    
        "problem",
    )
    permission_required = ("maintenance.add_maintenancerequest",)
    success_message = _('maintenance request added successfully.')
    template_name = "maintenance/add_maintenance_request.html"
    extra_context = {"title": _("Add maintenance requests")}
    
    def get_success_url(self):
        print(self.object)
        return reverse_lazy(
            "maintenance:list_maintenancerequests",
        )


class ListMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin,  ListView):
    """list maintenance request view """

    model = MaintenanceRequest
    permission_required = ("maintenance.view_maintenancerequest",)
    template_name = "maintenance/list_maintenance_request.html"
    context_object_name = 'maintenance_requests'
    extra_context = {"title": _("List maintenance requests")}
    
    def get_queryset(self):
        return self.model.objects.filter(is_approved=False, is_declined = False, is_request=True)
    
    
    

class UpdateMaintenanceRequestView(UpdateView, PermissionRequiredMixin, SuccessMessageMixin):
    """ update maintenance request view """
    
    model = MaintenanceRequest
    fields = (
        "item",
        "quantity",
        "problem",
    )
    permission_required = "maintenance.change_maintenancerequest"
    template_name = "maintenance/update_maintenace_request.html"
    success_message = 'Maintenance request of %(item)s updated successfully.'
    success_url = reverse_lazy("maintenance:list_maintenacerequests")
    context_object_name = "update_maitenance"
    extra_context = {"title": _("Update Maintenance Request")}
    
    
class CancelMaintenanceRequestView(UpdateView, PermissionRequiredMixin, SuccessMessageMixin):
    """ cancel request view """
    
    model = MaintenanceRequest
    
    fields = ("is_request")
    permission_required = "maintenance.cancel_maintenancerequest"
    success_url = reverse_lazy("maintenance:canceled_list")
    success_message = "Maintenance request cancelled successfully"
    http_method_names = ["post"]
    
    def get_form_kwargs(self):
        print("HEY")
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({ "is_request" : False})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        print("AM FROM CANCAEL")
        return self.model.objects.filter(is_request=True)
    
class CanceledListMaintenanceRequestView(PermissionRequiredMixin, ListView, SuccessMessageMixin):
    model = MaintenanceRequest
    permission_required = "view_canceled_maintenancerequest"
    template_name = "maintenance/canceled_list_request.html"
    context_object_name = "canceled_request"
    extra_context = {"title": "Canceled Maintenance Request" }
    
    def get_queryset(self):
        return self.model.objects.filter(is_request=False)
    


    
class ApproveMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
    """Generic view used to approve request"""
    
    model =  MaintenanceRequest
    fields = ("is_approved",)
    permission_required = "maintenance.can_approve"
    success_url = reverse_lazy("maintenance:lists_approved_request")
    success_message = "Maintenance request approved successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_approved": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_approved=False)
    

class ListApprovedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
        """list of approved (undermaintenace ) request view """
    
        model =  MaintenanceRequest
        template_name = "maintenance/lists_undermaintenance.html"
        permission_required = "maintenance.view_list_approved_maintenance_request"
        extra_context = {"title": _("Approved Maintenance Request")}
        context_object_name = "list_approved"
        
        def get_queryset(self):
            return self.model.objects.filter(is_approved=True,is_damaged=False)
        
         
class DeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to declined request"""
    model =  MaintenanceRequest
    fields = ("is_declined",)
    permission_required = "maintenance.can_decline"
    success_url = reverse_lazy("maintenance:lists_declined_request")
    success_message = "Maintenance request declined successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_declined": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_declined=False)
    
      

    
class ListDeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    """Generic view used to declined request list"""

    model =  MaintenanceRequest
    template_name = "maintenance/declined_list.html"
    permission_required = "maintenance.view_list_declined_maintenance_request"
    context_object_name = "list_declined"
    extra_context = {"title": _("Declined Maintenance Request")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_declined=True)
        
    """generic view for repaired item list """
    
class RepairedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
         model =  MaintenanceRequest
         itemName = "item.item.is_repair"
         fields = ("",)
         permission_required = "maintenance.can_repaire"
         success_url = reverse_lazy("Store:list_items")
         success_message = " Items request repaired successfully"
         http_method_names = ["post"]
         
         def get_form_kwargs(self):
             form_kwargs = super().get_form_kwargs()
             form_data = form_kwargs.get("data", {}).copy()
             form_data.update({"is_repaired": True})
             form_kwargs.update({"data": form_data})
             return form_kwargs
         
         def get_queryset(self):
                return self.model.objects.filter(is_repaired=False)

class ListRepairedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    
    model =  MaintenanceRequest
    template_name = "maintenance/list_repaired_maintenace.html"
    permission_required = "maintenance.view_list_repaired_maintenance_request"
    context_object_name = "list_declined"
    extra_context = {"title": _("Declined Maintenance Request")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_declined=True)
        
    
    

class AddFailurityReportView(CreateView, PermissionRequiredMixin, SuccessMessageMixin):
    """ Add failurity report view  """
    
    model = FailurityReport
    fields = "__all__"
    permission_required = ("maintenance.add_failurityreport",)
    success_message = _('failurity reports added successfully.')
    template_name = "maintenance/add_failurity_report.html"
    success_url = reverse_lazy("maintenance:list_failurity_report")
    extra_context = {"title": _("Add FailurityReport")}
    


class ListFailurityReportView(ListView, PermissionRequiredMixin, SuccessMessageMixin):
    """" list for failurity report view  """
    
    model = FailurityReport
    permission_required = ("maintenance.view_failurityreport",)
    template_name = "maintenance/list_failurity_report.html"
    context_object_name = "failurity_reports"
    extra_context = {"title": _("list failurity reports")}

"""" detail failurity report view  """

class DetailFailureReprtView(DetailView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    permission_required = ("maintenance.view_failurity_report",)
    template_name = "maintenance/detail_failure_report.html"
    context_object_name = "failurereport"
    extra_context = {"title": _("Detail failurity reports")}
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    


class AddDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Add damage report from item directly. """
    
    model = DamageReport
    fields = "__all__"
    permission_required = ("maintenance.add_damagereport",)
    success_message = _('Damage reports added successfully.')
    template_name = "maintenance/add_damage.html"
    success_url = reverse_lazy("maintenance:list_damagereports")
    context_object_name = "add_damage_report"

    extra_context = {"title": _("Add damage reports")}
    

class ListDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    """ Damage Report  list view direct from item. """
    
    model = DamageReport
    permission_required = ("maintenance.view_damagereport",)
    template_name = "maintenance/list_direct_damage.html"
    context_object_name = "damagereports"
    extra_context = {"title": _("list damage reports")}
    
    

class AddDamagedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """ Damaged maintenance report item list from under maintenance (approved item) """
    
    model = MaintenanceRequest
    x = [ i for i in MaintenanceRequest._meta.get_fields()]
    print(type(x[1]))
    fields = ("is_damaged",)
    permission_required = "maintenance.can_damagemaintenancerequest"
    success_url = reverse_lazy("maintenance:damaged_requests_lists")
    success_message = "Damage report added successfully"
    http_method_names = ["post"]
   
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_damaged": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_damaged=False)
    
class ListDamagedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    model = MaintenanceRequest
    template_name = "maintenance/list_damage_maintenance.html"
    permission_required = "maintenance.view_listdamagedmaintenacerequest"
    context_object_name = "list_damaged_maintenance_request"
    extra_context = {"title": _("Damaged Item")}
    
    def get_queryset(self):
            return self.model.objects.filter(is_damaged=True)
        
        