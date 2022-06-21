from django.shortcuts import render
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
    fields = "__all__"
    permission_required = ("maintenace.add_maintenacerequest",)
    success_message = _('maintenace request added successfully.')
    template_name = "maintenace/add.html"
    success_url = reverse_lazy("maintenace:list_maintenacerequests")
    extra_context = {"title": _("Add maintenace requests")}
    
    def name(request):
        if request.method == 'POST':
            form = AddMaintenaceRequest(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            return render(request, 'add.html', {'form': form, 'name': name, 'surname': surname })
        else:
            form = AddMaintenaceRequest()
            return render(request, 'list.html', {'form': form})
    
    

class ListMaintenaceRequestView(PermissionRequiredMixin, SuccessMessageMixin,  ListView):
    model = MaintenanceRequest
    permission_required = ("maintenace.view_maintenacerequest",)
    template_name = "maintenace/list.html"
    context_object_name = 'maintenance_requests'
    extra_context = {"title": _("List maintenace requests")}
    
    

class ApproverMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to approve request"""
    
    model =  MaintenanceRequest
    fields = ("is_approved",)
    success_url = reverse_lazy("maintenace:list_undermaintenaces")
    success_message = "Maintenace request approved successfully"
    http_method_names = ["post"]
   
    def form_valid(self, form):
        form.instance.is_approved = True
        return super().form_valid(form)
    
    def get_queryset(self):
        return self.model.objects.filter(is_approved=False)
    

class ListApprovedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
        model =  MaintenanceRequest
        template_name = "maintenace/approved_list.html"
        permission_required = "maintenace.view_list_approved_maintenance_request"
        extra_context = {"title": _("Approved Maintenance Request")}
        context_object_name = "list_approved"
        
         
class DeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Generic view used to declined request"""
    
    model =  MaintenanceRequest
    fields = ("is_declined","problem")
    success_url = reverse_lazy("maintenace:list_undermaintenaces")
    success_message = "Maintenace request declined successfully"
    http_method_names = ["post"]
   
    def form_valid(self, form):
        form.instance.is_declined = True
        return super().form_valid(form)
    
    def get_queryset(self):
        return self.model.objects.filter(is_declined = False)



class ListDeclinedMaintenanceRequestView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    """Generic view used to declined request list"""
    
    model =  MaintenanceRequest
    model = MaintenanceRequest
    template_name = "maintenace/declined_list.html"
    context_object_name = 'list_declined_requests'
    extra_context = {"title": _("List_declined_maintenace_requests")}
    



class  ListUnderMaintenaceView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    
    model =  MaintenanceRequest
    fields = "__all__"
    permission_required = ("maintenace.view_undermaintenace",)
    template_name = "maintenace/under.html"
    success_url = reverse_lazy("maintenace:list_undermaintenace")
    extra_context = {"title": _("Under maintenace requests")}
    
""""ADD failurity report view  """

class AddFailurityReportView(CreateView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    fields = "__all__"
    permission_required = ("maintenace.add_failurityreport",)
    success_message = _('%(item)s reports added successfully.')
    template_name = "maintenace/add_failurity_report.html"
    success_url = reverse_lazy("maintenace:list_failurity_report")
    extra_context = {"title": _("Add FailurityReport")}
    
"""" list for failurity report view  """

class ListFailurityReportView(ListView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    permission_required = ("maintenace.view_failurity_report",)
    template_name = "maintenace/failurityreportlist.html"
    context_object_name = "failurity_reports"
    extra_context = {"title": _("list failurity reports")}

""""detail failurity report view  """

class DetailFailureReprtView(DetailView, PermissionRequiredMixin, SuccessMessageMixin):
    
    model = FailurityReport
    permission_required = ("maintenace.view_failurity_report",)
    template_name = "maintenace/failurityreportlist.html"
    context_object_name = "failurereport"
    extra_context = {"title": _("Detail failurity reports")}
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
      

# """Add damage report """
# class AddDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = DamageReport
    
#     fields = "__all__"
#     permission_required = ("maintenace.add_damagereport",)
#     success_message = _('Damage reports added successfully.')
#     template_name = "maintenace/add.html"
#     success_url = reverse_lazy("maintenace:list_damagereports")
#     extra_context = {"title": _("Add damage reports")}
    
# "Damage Report list view"
# class ListDamageReportView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
#     model = DamageReport
#     permission_required = ("maintenace.view_damagereport",)
#     template_name = "maintenace/damagereportlist.html"
#     context_object_name = "damagereports"
#     extra_context = {"title": _("list damage reports")}



      
# class AddUnderMaintenanceView(CreateView, PermissionRequiredMixin, SuccessMessageMixin):
    
#     model = UnderMaintenace
#     fields = "__all__"
#     permission_required = ""
#     template_name = "maintenace/under.html"
#     extra_context = {"title": _("Under Maintenance Item")}
#     context_object_name = "undermaintenance_item"
    
    
#     def get_queryset(self):
#         return self.model.objects.filter(is_approved=True)
        
    
    