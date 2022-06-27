from email.policy import default
from itertools import permutations
from unicodedata import name
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from store.models import Item, Store

      
""" Creating failurity report model"""        
       
class FailurityReport(models.Model):
    item = models.ForeignKey(
                             Item,
                             on_delete=models.CASCADE,
                             verbose_name=_("items"),
                             related_name="failurityreports",
                             
                             )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)]) # dont forget to add maximum
    
    problem = models.TextField(_("problem"))
        
    class Meta:
        verbose_name = _("failurityreport")
        verbose_name_plural = _("failurityreports")
         

    def __str__(self):
        return f"{self.item.name}"


""" Models for maintenace request """    
    
class MaintenanceRequest(models.Model):
    item = models.ForeignKey(
                             FailurityReport,
                             on_delete=models.CASCADE,
                             verbose_name=_("Item from failures"),
                             related_name="maintenacerequests"
                             )
    
    problem = models.TextField(_("problem"),null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)  #don't forget to do max validator
    is_declined = models.BooleanField(default=False)
    is_request = models.BooleanField(default=True)
    is_repaired = models.BooleanField(default=False)
    is_damaged = models.BooleanField(default=False)
    decline_reason = models.TextField(null=True)

    class Meta:
        verbose_name = _("maintenance request")
        verbose_name_plural = _("maintenance requests")
        
        
    def __str__(self):
        return self.item.item.name
 
 
 
class DamageReport(models.Model):
    
    item = models.ForeignKey(
		Item,
		on_delete = models.CASCADE,
        verbose_name =_("item"),
        related_name = "damagereport",
        
        )
    
    undermaintenance = models.ForeignKey(
                                        MaintenanceRequest,
                                        on_delete=models.CASCADE,
                                        verbose_name="under maintenance",
                                        null=True
                                        
    )
    
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1),], )
    problem = models.TextField(null=False, error_messages={"fill": "You should specify the problem."} )
    is_damaged = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("damagereport")
        verbose_name_plural = _("damagereports")
    
    def __str__(self):
        return self.item.name

