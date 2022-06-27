from concurrent.futures import process
from datetime import datetime
from pickle import TRUE
from pyclbr import Class
from shelve import Shelf
from tracemalloc import start
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from auser.models import Department
# from auser.models import Staffmember 
from django.utils.translation import gettext as _
from django.conf import settings


#from request.validator import MaxValueValidator
timezone.localtime(timezone.now())
from django.contrib.auth.models import User
from django.utils.duration import _get_duration_components

from store.models import Item, Store 

User = settings.AUTH_USER_MODEL

STATUS = ((0, "Draft"), (1, "Publish"))



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
    is_approved = models.BooleanField(null=True, blank=True)  # decline--false, approve--true, pending--null
    is_given = models.BooleanField(null=True, blank=True)     # for store officer item delivered--True or borowed
    is_returned = models.BooleanField(default=False )         # when item back to store is_returned--True
    requesting = models.BooleanField( default= False)         # True-- item is requested
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
                                    on_delete=models.CASCADE,    )   # TODO: dont forget set null value for user
    
    # approved_time = models.DateTimeField(datetime.now)@propert   
    

    @property
    def itemQuantity(self):
        return self.item.quantity  
    quantity = models.IntegerField(validators=[MaxValueValidator(int(23))],)    # max validation is not working
  
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        permissions = [                   
                       ('can_cancel_request', 'Can cancel request'),
                       ('can_approve_request', 'Can approve request'),
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
                
                ]
        ordering = ("-id",)

    def __str__(self):
        return self.item.name

    
