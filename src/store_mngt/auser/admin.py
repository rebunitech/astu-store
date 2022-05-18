from django.contrib import admin

from .models import Department, School, Storekeeper

admin.site.register(Department)
admin.site.register(School)
admin.site.register(Storekeeper)