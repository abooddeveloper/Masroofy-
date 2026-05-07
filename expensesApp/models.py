from django.db import models
from django.utils import timezone
from register_login.models import userRegistration
# Ceate your models here.



class Cycle(models.Model):
    user = models.OneToOneField(userRegistration,on_delete=models.CASCADE,null=True,blank=True)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now)
    total_allowance=models.DecimalField(max_digits=10,decimal_places=2)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.user.username+' '+str(self.start_date)+'----'+ str(self.end_date)


class Category(models.Model):
    user = models.ForeignKey(userRegistration,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,null=False,blank=False)
    icon=models.ImageField(null=True,blank=True,upload_to='',default='anchor.png')
    
    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name



class Expense(models.Model):
    user = models.ForeignKey(userRegistration,on_delete=models.CASCADE,null=True,blank=True)
    cycle=models.ForeignKey(Cycle,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=20,decimal_places=2)
    time_stamp=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-time_stamp']



    def __str__(self):
        return str(self.time_stamp)+"--"+self.category.name
