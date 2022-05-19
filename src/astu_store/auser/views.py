from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "auser/dashboard.html"
    extra_context = {"title": _("Dashboard")}
