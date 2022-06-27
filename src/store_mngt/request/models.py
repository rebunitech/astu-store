from concurrent.futures import process
from datetime import datetime
from pickle import TRUE
from pyclbr import Class
from shelve import Shelf
from tracemalloc import start
from webbrowser import get
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from auser.models import Department
from django.utils.translation import gettext as _
from django.conf import settings
timezone.localtime(timezone.now())
from django.utils.duration import _get_duration_components
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS = ((0, "Draft"), (1, "Publish"))


class Store(models.Model):
    dept_status = (
        ("CSE", "CSE"),
        ("ECE", "ECE"),
        ("EPCE", "EPCE"),
    )
    department = models.CharField(choices=dept_status, max_length=100)
    block = models.IntegerField(blank=True, null=True)
    room = models.IntegerField(blank=True, null=True)
    remark = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"B:{self.block} R:{self.room}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    DSN = models.CharField(max_length=150)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,default=True,null=True)
    year = models.DateTimeField(default=True)
    supplier = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):  
        return self.name[:10]
     

class Request(models.Model):

    STATUS = (
        ("consumable", "consumable"),
        ("non-consumable", "non-consumable"),
    )
    
    item = models.ForeignKey(
                            Item,
                             on_delete=models.CASCADE,
                             related_name="request",
                             verbose_name="Item"
                             ) 
    
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=100, choices=STATUS)
    status = models.CharField(max_length=30)
    is_approved = models.BooleanField(null=True, blank=True) 
    is_given = models.BooleanField(null=True, blank=True)     
    is_returned = models.BooleanField(null=True , blank=True )        
    department = models.ForeignKey(
                                    Department,
                                    on_delete=models.CASCADE,
                                    verbose_name="department",
                                    related_name="requests",
                                    
    )
    requester = models.ForeignKey(
                                    User, 
                                    db_constraint=False , 
                                    null=True, related_name='staff',
                                    verbose_name="staffmember",
                                    on_delete=models.CASCADE,    )   
    is_requesting = models.BooleanField(default=True)   
    quantity = models.IntegerField()  
   

    class Meta:
        permissions = [                   
                       ('can_cancel_request', 'Can cancel request'),
                       ('can_approve_request', 'Can approve request'),
                       ('can_delete_request', 'Can delete request'),
                       ('can_decline_request', 'Can decline request'),
                       ('can_complete_request', 'Can complete request'),
                       ('can_return_request', 'Can return request'),
                       ('can_process_request', 'Can process request'),
                       ('can_view_request_list', 'Can view request list'),
                       ('can_view_request_detail', 'Can view request detail'),
                       ('can_view_request_cancel', 'Can view request cancel'),
                       ('can_view_request_approve', 'Can view request approve'),
                       ('can_view_request_decline', 'Can view request decline'),
                       ('can_view_request_complete', 'Can view request complete'),
                       ('can_view_request_return', 'Can view request return'),
                       ('can_view_processed_request','Can view processed request'),
                       ('can_view_borrow_detail', 'Can view borrow detail'),
                        ('view_item', 'Can view borrow detail'),
                        ('can_view_request_history', 'Can view request history'),
                       
                
                ]
        ordering = ("-id",)

    def __str__(self):
        return self.item.name

   
        
    
