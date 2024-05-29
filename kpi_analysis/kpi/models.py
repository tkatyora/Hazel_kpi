from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import pandas as pd




def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.csv', '.xlsx']
  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Unsupported file type!')
  

def validate_site_name_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.xlsx']
  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Unsupported file type!')


      

class User(AbstractUser):
        role = [
            ('technition', 'Technician'),
            ('team-leader', 'Team Leader'),
            ('admin', 'Analysis Manager'),
          
          
            ]
        
        CITY_CHOICES = [
             ('none', '-----------'),
            ('section_a', 'Midland A'),
            ('section_b', 'Midlands B'),
            ]
        region_choices= [
              ('None', '----------'),
            ('region1', 'Midland and Manicaland'),
            ('region2', 'Harare and Bulawayo'),
            ]
    
        phoneNumber  = models.CharField(null=True,blank=True,max_length=12)
        city = models.CharField(max_length=255,null=True,blank=True,choices=CITY_CHOICES)
        region = models.CharField(max_length=255,null=True,blank=True,choices=region_choices)
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
        Problem = [
            ('No-Power', 'No Power'),
            ('No-Solar', 'No Solar'),
             ('Functions', 'Events Going On'),
            ('Public-Holiday', 'Public Holidays'),
            
          
            ]
      
        body= models.TextField(null=True,blank=True)
        types = models.CharField(max_length=100,null=True,default='Not Selected' ,choices=type , blank= False)
        analysisfile = models.FileField(upload_to='', max_length=255,null=True)
        created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
        created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)
        problem = models.CharField(max_length=100,null=True,default='Not Selected' ,choices=Problem , blank= False)
        
       
        @property
        def FileUrl(self):
            try:
                url = self.analysisfile.url
            except:
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

    def save(self,*args , **kwargs):
        data  = self.file
        df = pd.read_excel(data)
        df['SiteCode'] = df['SITE Name']
        df['ServiceRate'] = df['306004:TCH in service rate(%)']
        df['TotalTraffic'] = df['306024:TCH total traffic number(erl)']
        df['PSData'] = df['900134113:U31_Aggregate PS Data (MB)_900134_1_gv4.bsc-MO']
        #Data Cleaning
        df_missing = df.dropna()
        #Check Completenes 
        nan_counts_per_column = df.isna().sum(axis=0)
        total_rows = df.shape[0]
        percent_missing_column = (nan_counts_per_column / total_rows) * 100
        print(percent_missing_column)
        #Duplicates
        duplicates = df_missing.duplicated()
        duplicates
        df_duplicates = df_missing.drop_duplicates()
        try:
            df_duplicates['Begin Time'] = pd.to_datetime(df_duplicates['Begin Time'], format='%Y-%m-%d')
            df_duplicates['End Time'] = pd.to_datetime(df_duplicates['End Time'], format='%Y-%m-%d ')
        except ValueError:  
            try:
                df_duplicates['Begin Time'] = pd.to_datetime(df_duplicates['Begin Time'])
                df_duplicates['End Time'] = pd.to_datetime(df_duplicates['End Time'])
            except pd.errors.ParserError:  
                    print("Warning: Could not automatically convert 'Begin Time' and 'End Time' columns to datetime format")

        df_drop = df_duplicates[['Begin Time','End Time','Granularity','Managed Element','SiteCode','BTS Name','ServiceRate','TotalTraffic']]
        print(df_drop.shape)
        df_site_name = pd.read_excel('CleanedData/siteNameCleaned.xlsx')
        df_merged = df_drop.merge(df_site_name, on='SiteCode', how='left')
        print(df_merged.shape)
        if 'Site Code' in df_merged.columns:
            df_merged['SiteCode'] = df_merged['SiteCode'].fillna(df_merged['SiteCode'],inplace =True)  

        df_duplicate = df_merged.drop_duplicates()
        print(df_duplicate.shape)
        df_miss = df_duplicate.dropna()
        print(df_miss.shape)
        df_analysis = df_duplicate
        print(df_analysis.shape)
        df_analysis.to_excel('CleanedData/CleanedDataset.xlsx' ,index=False)
        super().save(*args,**kwargs)

    def __str__(self):
                return f" DataSet for {()} "

class SiteName(models.Model):      
    file = models.FileField(upload_to='', max_length=255,null=True,validators=[validate_site_name_extension])
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
    created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)


    def save(self,*args , **kwargs):
        site  = self.file
        df_site_name = pd.read_excel(site)
        df_site_name['SiteCode']= df_site_name['Unnamed: 0']
        df_site_name['SiteName']= df_site_name['Unnamed: 1']
        df_site = df_site_name[['SiteCode','SiteName']]
        print('Before duplicates removal',df_site.shape)
        df_duplicates = df_site.drop_duplicates()
        print('After Duplicates Removal',df_duplicates.shape)
        print('Before missing values removal',df_duplicates.shape)
        df_missing = df_duplicates.dropna()
        print('After missing Removal',df_missing.shape)

        df_site_final = df_missing 

        df_site_final.to_excel('CleanedData/siteNameCleaned.xlsx' ,index=False)
       
       

        super().save(*args,**kwargs)

       
    def __str__(self):
            return f" DataSet for {(self.file)} "
        
class AnalysisVaribales(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
    created_on = models.DateTimeField( auto_now=False, auto_now_add=True ,null=True)
    def __str__(self):
            return f" Analysis of : {(self.name)} "
        