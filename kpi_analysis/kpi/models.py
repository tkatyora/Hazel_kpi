from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError




def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.csv', '.xlsx']
  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Unsupported file type!')



class city(models.Model):
      name = models.CharField(max_length=100)
      def __str__(self):
                return f" City of : {(self.name)} "
      

class User(AbstractUser):
        role = [
            ('technition', 'Technition'),
            ('supervisor', 'Anaysis Supervisor'),
            ('admin', 'Analysis Manager'),
          
          
            ]
        
        CITY_CHOICES = [
            ('Harare', 'Harare'),
            ('Bulawayo', 'Bulawayo'),
            ('Gweru', 'Gweru'),
            ('Chitungwiza', 'Chitungwiza'),
            ('Mutare', 'Mutare'),
            ('Kwekwe', 'Kwekwe'),
            ('Kadoma', 'Kadoma'),
            ('Masvingo', 'Masvingo'),
            ('Norton', 'Norton'),
             ('Chinhoyi', 'Chinhoyi'),

            ]
    
        phoneNumber  = models.CharField(null=True,blank=True,max_length=12)
        city = models.ManyToManyField(city, blank=True)
        econetNumber = models.CharField(max_length=200,null=True ,blank= True)
        profilePicture = models.ImageField(upload_to ='Pictures', blank=True ,null= True) 
        roles = models.CharField(max_length=255, unique=False,choices=role,null=True,blank=True)
        is_admin = models.BooleanField(default=False, null = True)
        is_technition = models.BooleanField(default=False, null = True)
        is_supervisor = models.BooleanField(default=False, null = True)
        groups = models.ManyToManyField('auth.Group', related_name='User_user_set', blank=True)
        user_permissions = models.ManyToManyField('auth.Permission', related_name='User_user_set', blank=True)

       
        @property
        def ImageUrl(self):
            try:
                url = self.profilePicture.url
            except ValueError:
                url = ''
            return url
      
        def __str__(self):
                return f"Information for : {(self.username)} "
        


        
class CommentReports(models.Model):
        type = [
            ('comment', 'Comment'),
            ('decision', 'Decision'),
             ('report', 'Report'),
            ('finaldecision', 'Final Decision'),
            
          
            ]
      
        body= models.TextField(null=True,blank=True)
        types = models.CharField(max_length=100,null=True,default='Not Selected' ,choices=type , blank= False)
        analysisfile = models.FileField(upload_to='', max_length=255,null=True,validators=[validate_file_extension])
        fullReportFile = models.FileField(upload_to='', max_length=255,null=True,validators=[validate_file_extension])
        created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
        created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)
        Picture = models.ImageField(upload_to ='Pictures', blank=True ,null= True)
        
        @property
        def ImageUrl(self):
            try:
                url = self.Picture.url
            except ValueError:
                url = ''
            return url

       
        def __str__(self):
                return f" Final Comment Created by : {(self.created_by.username)} "
        

class DataSet(models.Model):
    type = [  
          ('xlsx', 'Excel Format'),
            ('csv', 'CSV(Comma SEparated Values) Format'),
          ]
      
        
    types = models.CharField(max_length=100,null=True,default='Not Selected' ,choices=type , blank= False)
    file = models.FileField(upload_to='', max_length=255,null=True,validators=[validate_file_extension])
    name = models.CharField(max_length=50,null=True,blank=True)	
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
    created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)

    def __str__(self):
                return f" DataSet for {(self.name)} "





class AnalysisVaribales(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
    created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)
    def __str__(self):
            return f" Analysis of : {(self.name)} "
        