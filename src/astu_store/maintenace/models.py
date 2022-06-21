from itertools import permutations
from unicodedata import name
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from store.models import Item, Store

      
"""failurity report model"""     
       
class FailurityReport(models.Model):
    item = models.ForeignKey(
                             Item,
                             on_delete=models.CASCADE,
                             verbose_name=_("items"),
                             related_name="failurityreports"
                             )
    quantity = models.IntegerField(validators=[MinValueValidator(0)]) # dont forget to add maximum
    
    problem = models.TextField(_("problem"))
        
    class Meta:
        verbose_name = _("failurityreport")
        verbose_name_plural = _("failurityreports")
        
       
        
    def __str__(self):
        return self.item.name



""" Models for maintenace request """    
    
class MaintenanceRequest(models.Model):
    item = models.ForeignKey(FailurityReport,
                             on_delete=models.CASCADE,
                             verbose_name=_("failurityreports"),
                             related_name="maintenacerequests"
                             )
    
    problem = models.TextField(_("problem"),null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    is_declined = models.BooleanField(default=False)


    
    class Meta:
        verbose_name = _("failurityreport")
        verbose_name_plural = _("failurityreports")
    
    def __str__(self):
        return self.item.name
 
 
# class DamageReport(models.Model):
#     item_name = models.ForeignKey(
# 		Item,
# 		on_delete = models.CASCADE,
#         verbose_name =_("item"),
#         related_name = "damagereport"
#         )
    
#     description = models.TextField(_("description"),null=True, blank=True) 

#     problem = RichTextField()
    
#     class Meta:
#         verbose_name = _("damagereport")
#         verbose_name_plural = _("damagereports")
    
#     def __str__(self):
#         return self.name

