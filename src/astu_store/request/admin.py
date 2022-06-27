from django.contrib import admin

from .models import Item, Request, Store

admin.site.register(Request)
admin.site.register(Item)
admin.site.register(Store)
# admin.site.register(OtherDepartmentRequest)
