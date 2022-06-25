from django.contrib import admin

from .models import Department, School, Storekeeper, Staffmember, User, SchoolHead, DepartmentHead

admin.site.register(Department)
admin.site.register(School)
admin.site.register(Storekeeper)
admin.site.register(Staffmember)
admin.site.register(User)
admin.site.register(SchoolHead)
admin.site.register(DepartmentHead)