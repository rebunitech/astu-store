from django.views.generic import CreateView

from astu_inventory.apps.help.models import Help
from astu_inventory.apps.help.forms import HelpForm

class AddHelpView(CreateView):
    model = Help
    form_class = HelpForm
    template_name = "help/add.html"
