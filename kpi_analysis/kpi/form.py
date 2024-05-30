from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
import pandas as pd

df_analysis = pd.read_csv('CleanedData/JupyterCleanedDataset.csv')
section_a_mask = df_analysis['SiteCode'].between('MID0001', 'MID0100')
section_b_mask = df_analysis['SiteCode'].between('MID0101', 'MID0219')

section_a = df_analysis[section_a_mask]
section_b = df_analysis[section_b_mask]


#MODULES FORMS
class CreateUserForm(UserCreationForm):
    
    email = forms.EmailField(required=False , label='Enter  Email address',
                              widget=forms.EmailInput(
                                  attrs={
                                      'class':'form-control input',
                                       'type':'email'
                                     
                                  })),
    first_name = forms.CharField(required=True , label='Enter First Name',
                                 widget=forms.TextInput(
                                  attrs={
                                      
                                      'class':'form-control input',
                                       'spellcheck':"true",
                                       'type':'text'
                                  }
                              ))
    last_name = forms.CharField(required=True , label='Enter Surname' ,
                                 widget=forms.TextInput(
                                  attrs={
                                      
                                      'class':'form-control input',
                                       'spellcheck':"true",
                                       'type':'text'
                                  }
                              ))
    username = forms.CharField(required=False , label='Create username' ,
                                 widget=forms.TextInput(
                                  attrs={
                                      
                                      'class':'form-control input',
                                       'spellcheck':"true",
                                       'type':'text'
                                  }
                              ))
    econetNumber = forms.CharField(required=True , label='Enter Econet Number' ,
                                 widget=forms.TextInput(
                                  attrs={
                                      
                                      'class':'form-control input',
                                       'spellcheck':"true",
                                       'type':'text'
                                  }
                              ))
    roles = forms.ChoiceField(
        required=False,
        label='Select  Role',
        choices=User.role,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    
    city = forms.ChoiceField(label='Select Analysis Section', choices=User.CITY_CHOICES)
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['last_name','first_name','phoneNumber','roles','econetNumber','email','city','region'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1'] and self.cleaned_data['password2']:
            user.set_password(self.cleaned_data['password1'])  
        if commit:
            user.save()
        return user



class CommentForm(ModelForm):

    body = forms.CharField(required=True , label='Enter Final Comment /Decison' ,
                                 widget=forms.TextInput(
                                  attrs={
                                      
                                      'class':'form-control input',
                                       'spellcheck':"true",
                                       'type':'text',
                                       'rows':2,
                                       'cols':1,
                                  }
                              )),
    types = forms.ChoiceField(
        required=False,
        label='Choose  Decision/ Report/ Final Decison',
        choices=CommentReports.type,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    problem = forms.ChoiceField(
        required=False,
        label='Choose  Reason',
        choices=CommentReports.Problem,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    analysisfile = forms.FileField(label= 'Upload The Graph',required=False, max_length=100,  widget=forms.FileInput(
                                attrs={
                                    'class':'form-control'
                                }
                            ))
    

    class Meta:
        model =CommentReports
        fields = ['body','types','analysisfile','problem'] 


class uploadDataForm(ModelForm):
    name =forms.CharField(label='Name of DataSet')
    file = forms.FileField(label= 'Upload Dataset',required=False, max_length=100,  widget=forms.FileInput(
                                  attrs={
                                       'class':'form-control'
                                  }
                              ),
                              help_text='Only Excel and CSV are Supported')
    types = forms.ChoiceField(
        required=True,
        label='Select  DataSet Format',
        choices=DataSet.type,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    def clean_file(self):
        
        file = self.cleaned_data.get('file') 
        selected_format = self.cleaned_data.get('types') 

        if file:
            import os
           
            ext = os.path.splitext(file.name)[1].lower()  
            valid_extension = '.csv' if selected_format == 'csv' else '.xlsx' 

            if ext != valid_extension:
                raise ValidationError(u'File extension does not match the selected format!')

        return file

    
    class Meta: 
        model = DataSet
        fields =['file','name','types']

class uploadSiteForm(ModelForm):
    file = forms.FileField(label= 'Upload Site Name',required=False, max_length=100,  widget=forms.FileInput(
                                  attrs={
                                       'class':'form-control'
                                  }
                              ),
                              help_text='Only Excel  Supported')    
    class Meta: 
        model = SiteName
        fields =['file']
    



class AnayasisKpiForm(forms.Form):
    choice = [('Time','Time'),
              ]
    versus = forms.ChoiceField(
        required=False,
        label='Aganist',
        choices=choice,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    variable_choices = [(variable.name, variable.name) for variable in AnalysisVaribales.objects.all()]
    variable = forms.ChoiceField(
        required=False,
        label='Variable',
        choices=variable_choices,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    
 




class AnayasisVariablesForm(ModelForm):
    name =forms.CharField(label='Name of Variable')
    class Meta: 
        model = AnalysisVaribales
        fields =['name']



class ServiceForm(forms.Form):
    traffic = [('high','High'),
                 ('low','Low')]
    Region_a = [('Gweru Athlone',' Gweru Athlone'),
                 ('Milsonia','Milsonia'),
                 ('Rothbat Building','Rothbat Building'),
                 ('Kwekwe Polytechnic','Kwekwe Polytechnic'),
                 ('Gweru CABS','Gweru CABS'),
                 ('Mambo','Mambo'),
                 ('Anderson School','Anderson School'),
                 ('Connemara','Connemara')]
    Region_b = [('Midlands State University 2','Midlands State University 2'),
                 ('Gokwe 3','Gokwe 3'),
                 ('Rothbat Building','Rothbat Building'),
                 ('Nyama','Nyama'),
                 ('Shurugwi Town','Shurugwi Town'),
                 ('Zvishavane Town','Zvishavane Town'),
                 ('Chiodza USF ','Chiodza USF'),
                 ('Gangata','Gangata')]
    service = [('low','Low[0 to 50%]'),
                 ('high','High [ 51 to 100%]'),
    ]
    chart = [('pie','Pie Chart'),
        ('bar','Bar Graph'),
                 
                 ]
    Traffic =forms.ChoiceField(choices=traffic, 
                             label='Traffic',
                            required=False)
    Service =forms.ChoiceField(choices=service, 
                            label='Service Rate',
                            required=False)
    Charts =forms.ChoiceField(choices=chart, 
                            label='Data visualization charts',
                            required=False)
    region_a = forms.ChoiceField(choices=Region_a, 
                            label='Select Analysis Area',
                            required=False)
    region_b = forms.ChoiceField(choices=Region_b, 
                            label='Select Analysis Area',
                            required=False)
    traffic_1 = forms.IntegerField(label='Start Traffic',
                            required=False)
    traffic_2 = forms.IntegerField(label='End Traffic',
                            required=False)
    service_1 = forms.DecimalField(label='Start Service',
                            required=False)
    service_2 = forms.DecimalField(label='End Service',
                            required=False)
    




class SelectForm(forms.Form):
    choice = [
              ('ServiceRate','Service Rate'),
              ('TotalTraffic','Total Traffic')]

    select =forms.ChoiceField(choices=choice, 
                             label='Select',
                            required=False)

        


        
