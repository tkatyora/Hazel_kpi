from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *



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
    city_choices = [(city.name, city.name) for city in city.objects.all()]
    city = forms.MultipleChoiceField(label='Select Analysis City', choices=city_choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        #fields = '__all__'
        fields = ['last_name','first_name','phoneNumber','roles','econetNumber','email','city'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1'] and self.cleaned_data['password2']:
            user.set_password(self.cleaned_data['password1'])  # Set password only if provided
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
                                       'rows':5,
                                       'cols':5,
                                  }
                              )),
    types = forms.ChoiceField(
        required=True,
        label='Choose  Decision/ Report/ Final Decison',
        choices=CommentReports.type,
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
    fullReportFile = forms.FileField(label= 'Full Report',required=False, max_length=100,  widget=forms.FileInput(
                                attrs={
                                    'class':'form-control'
                                }
                            ))
    

    class Meta:
        model =CommentReports
        fields = ['body','types','analysisfile','fullReportFile'] 


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
    



class AnayasisKpiForm(ModelForm):
    variable_choices = [(variable.name, variable.name) for variable in AnalysisVaribales.objects.all()]
    variable = forms.ChoiceField(
        required=True,
        label='Select  Analysis KPI',
        choices=variable_choices,
        widget=forms.Select(
            attrs={
                'class': 'form-control input',
            }
        )
    ) 
    
    class Meta: 
        model = DataSet
        fields =['variable']




class AnayasisVariablesForm(ModelForm):
    name =forms.CharField(label='Name of Variable')
    class Meta: 
        model = AnalysisVaribales
        fields =['name']
        
        
