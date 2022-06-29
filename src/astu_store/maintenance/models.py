from email.policy import default
from itertools import permutations
from unicodedata import name
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from inventory.models import Item, Store

      
"""failurity report model"""        
       
class FailurityReport(models.Model):
    item = models.ForeignKey(
                             Item,
                             on_delete=models.CASCADE,
                             verbose_name=_("items"),
                             related_name="failurityreports",
                             
                             )
    quantity = models.IntegerField(validators=[MinValueValidator(0)]) # dont forget to add maximum
    
    problem = models.TextField(_("problem"))
        
    class Meta:
        verbose_name = _("failurityreport")
        verbose_name_plural = _("failurityreports")
        
       
        

    # def save(self,*args,**kwargs):
    #     if self.item:
    #        Item.objects.filter(item__name=self.item).update(
    #            quantity=F('quantity') + self.quantity)
                          
    #     else:
    #         super(Item,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.item.name}"


    
class MaintenanceRequest(models.Model):
    """ Models for maintenance request """    
    
    item = models.ForeignKey(
                             FailurityReport,
                             on_delete=models.CASCADE,
                             verbose_name=_("Item from failures"),
                             related_name="maintenancerequests"
                             )
    
    problem = models.TextField(_("problem"),null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1,null=False)  #don't forget to do max validator
    is_declined = models.BooleanField(default=False)
    is_request = models.BooleanField(default=True)
    is_repaired = models.BooleanField(default=False)
    is_damaged = models.BooleanField(default=False)

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
        related_name = "damagereport"
        )
    
    # description = models.TextField(_("description"),null=True, blank=True) 
    quantity = models.IntegerField(validators=[MinValueValidator(1),], )
    problem = models.TextField(null=False, error_messages={"fill": "You should specify the problem."} )
    is_damaged = models.BooleanField(default=False)
    class Meta:
        verbose_name = _("damagereport")
        verbose_name_plural = _("damagereports")
    
    def __str__(self):
        return self.name

