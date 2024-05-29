from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .form import *
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.ioff()


# VARIABLES
users = User.objects.all()
df_analysis = pd.read_excel('CleanedData/JupyterCleanedDataset.xlsx')
section_a_mask = df_analysis['SiteCode'].between('MID0001', 'MID0100')
section_b_mask = df_analysis['SiteCode'].between('MID0101', 'MID0219')

section_a = df_analysis[section_a_mask]
section_b = df_analysis[section_b_mask]


comments = CommentReports.objects.all()
final = CommentReports.objects.filter(types='finaldecision').order_by('-created_on').first()

                                        # PROJECT OBJECTIVES

#---------------------------OBJECTIVE 1 USER AUTHENTICATION AND VALIDATION------------------------------
#1. To develop a system that enhance data integrity , validates and authenticate users
def signIn(request):
    if request.method == 'POST':
        print('in log in function')
        username = request.POST['username']
        password = request.POST['password']
        User = authenticate(request , username = username , password = password)
        print('authenticated succesfully')
        if User is not None:
            print('user is not none')
            login(request, User)
            print('log in')
            messages.success(request, 'Log  Successfully')
            return redirect('dashboard') 
        else:
            print('user is  none')
            messages.warning(request, 'Incorrect Domain Name or Password')
            return redirect('sign_in')
                      
    return render(request, 'sign_in.html' )

@login_required(login_url='sign_in') 
def AnalysisVariable(request):
    df_site = pd.read_excel('CleanedData/siteNameCleaned.xlsx')
    print(df_site.shape)
    analysis_form = AnayasisKpiForm()
    if request.method == 'POST':
        add_varible_form = AnayasisVariablesForm(request.POST)
        if add_varible_form.is_valid():
            form2= add_varible_form.save(commit=False)
            form2.created_by = request.user
            form2.save()
            messages.success(request, 'Variable Succesfully ')
        else:
            messages.success(request, 'Varibale not added')

    else:
        print("analysis varibale")
        add_varible_form = AnayasisVariablesForm()

    content ={}
    content ={ 
    'form':analysis_form,
    'form2':add_varible_form
    }
   
    return render(request, 'variable.html' ,content)
@login_required(login_url='sign_in')
def dashboard(request):
    content ={}
    content = {
        
   
    }  
    return render(request , 'dashboard.html',content)

@login_required(login_url='sign_in')
def signout(request):
    logout(request)
    messages.success(request, 'Log Out successfully')
    return redirect('sign_in')

@login_required(login_url='sign_in') 
def viewUser(request):
    content ={}
    content ={ 
    'users': users
    }
   
    return render(request, 'view_users.html' ,content)

@login_required(login_url='sign_in') 
def deleteUser(request, pk):
    user_to_delete = User.objects.get(id=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        print('user deleted success')
        messages.success(request, 'User Succesfully Deleted')
        return redirect('view_user')
    content = {}
    content = {
        'user': user_to_delete
        
    }
    return render(request, 'delete_user.html', content)


def ChangePassword(request):
    if request.method == 'POST':
        change_pass =PasswordChangeForm(user=request.user, data=request.POST)
        print('validating te change passowrd form')
        if change_pass.is_valid():
            change_pass.save()
            print('form is saved')
            update_session_auth_hash(request,change_pass.user)
            logout(request)
            mgs = f'''
                You have succefully changes the password.\n

                Log In With The New passowrd
                    '''
            messages.success(request, mgs)
            return redirect('sign_in')
        else:
            print('passowrd id not valid')
            messages.warning(request, 'Form is not Valid')
    else:
        change_pass =PasswordChangeForm(user=request.user)
         
    content ={}
    content ={ 
    'form': change_pass
    }
            
                      
    return render(request, 'change_password.html' ,content)



@login_required(login_url='sign_in') 
def addNewUser(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            print('The Regestration Function Excuted') 
            email = user_form.cleaned_data.get('email',None)
            name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            username = f'{name.lower()}.{last_name.lower()}'
            roles = user_form.cleaned_data['roles']
            econum =  user_form.cleaned_data['econetNumber']
            password = f'kpi+{econum}'
            print(password)
            user = user_form.save(commit=False)
            if roles == 'admin':
                user.is_admin = True
                print('user set to admin')
            elif roles == 'supervisor':
                user.is_supervisor = True
                print('user set to supervisor')
            elif roles == 'technition':
                user.is_technition = True
                print('user set to  is_technition')
            elif roles == 'analysis':
                user.is_is_analysis = True
                print('user set to  analysis Manager')
            print(username)
            user.username = username
            user.set_password(password)
            if user is not None:
                user.save()
                msg2 = f'{name} {last_name} is added Succefully with username {username}'
                messages.success(request, msg2)
                return redirect('dashboard')
            else:
                messages.success(request, 'User Already Exist')
                   
        else:
            for error in list(user_form.errors.values()):
                messages.warning(request,error)
                print('Form has following errors', error)
            

    else:
        print('Its a get Request')
        user_form = CreateUserForm()
        
    content ={}
    content ={ 
    'form': user_form
    }
    return render(request, 'add_user.html' , content)
        


#--- OBJECTIVE 4 CUSTOMIZABLE ANALYTICS AND VISUALIZATION ----------------------------------------
#     4. To develop a system that provide customizable analytics and visualization features on  KPI trends.
@login_required(login_url='sign_in')
def WholeAnalysis(request):
    print(request.method)
    form2 = SelectForm()
    if request.method == 'POST':  
        form_comment =CommentForm(request.POST)
        form = SelectForm(request.POST)
        if form.is_valid():
            selection = form.cleaned_data.get('select')
            selected_category = request.POST.get('category',None)
            if selected_category == 'Yes':
                print(selected_category)
                print('validating the comment form')
                if form_comment.is_valid():
                    bodys =  request.POST.get('comment', '')
                    print(bodys)
                    fm = form_comment.save(commit=False)
                    fm.created_by = request.user
                    fm.types = 'comment'
                    fm.body = bodys
                    fm.save()
                    print('form is saved')
                    print('form valid')
                    mgs = f'''
                        You have succefully Added a {fm.types}'''
                    messages.success(request, mgs)
                else:
                    print(f'form not valid not valid,{form_comment.errors}')
                    messages.warning(request, form_comment.errors)
    
            elif selected_category == 'No' or None:
                print(selected_category,'NO comment added')
        if request.user.city == 'section_a':
            df_grouped = section_a.groupby(df_analysis['End Time'])[selection].mean()
            a = 'Midlands Part A'
        elif request.user.city == 'section_b':
            df_grouped = section_b.groupby(df_analysis['End Time'])[selection].mean()
            a = 'Midlands Part B'
        print(selected_category)  
        print(request.user.city)     
        print(df_analysis.shape,'df analysis')
        print(df_grouped.shape,'df grouped')
        print(a)
        print(selection)
        
        time_interval = df_grouped.index.to_numpy()  
        average_service_rate = df_grouped.to_numpy()  
        plt.figure(figsize=(10, 5))  
        plt.plot(time_interval, average_service_rate)
        plt.xlabel('Time Interval')
        plt.ylabel(f'Average {selection}')
        plt.title(f'Average {selection} by Time Interval for {a}')
        plt.grid(True)
        plt.tight_layout()
        print('saving the imagie to static/Images/wholeanalysi.png')
        plt.savefig('static/Images/wholeanalysi.png')
        plt.close()
        
    else:
        form2 = SelectForm()
        form_comment =CommentForm()
        selection = 'TotalTraffic'
      
    content={}
    content = {
        'form2':form2,
        'form':form_comment
    }

    return render(request, 'wholeanalysis.html', content)



@login_required(login_url='sign_in')
def Analysis(request):
    print(request.method)
    
    print(request.user.city)
    if request.method == 'POST':
        print(request.method)
        print('post')
        print(request.user)
        form2 = ServiceForm(request.POST)
        form = AnayasisKpiForm(request.POST)
        if form2.is_valid():
            print(request.user)
            if request.user.city == 'section_a':
                Sitename = form2.cleaned_data.get('region_a')
                a = 'section a'
              
                print('in section a')
            elif request.user.city == 'section_b':
                Sitename = form2.cleaned_data.get('region_b')
                a = 'section b'
            else:
                Sitename = form2.cleaned_data.get('region_a')
                print('else')
                a = 'in else'
            
            if form.is_valid():
                variables = form.cleaned_data.get('variable')
    
           
            start_time = request.POST.get('enddate', None)
            end_time = request.POST.get('startdate', None)
            print(start_time)
            print(end_time)
            print(Sitename)
            
            df_name = df_analysis[df_analysis['SiteName'] == Sitename]
            mask = (df_name['Begin Time'] >= start_time) & (df_name['End Time'] <=  end_time)
            filtered_df = df_name .loc[mask]
            print('shape',df_name.shape)
            filtered_df.set_index('Begin Time', inplace=True)

            print(variables)
            plt.figure(figsize=(12, 5))
            plt.plot(filtered_df.index, filtered_df[variables])
            plt.xlabel('Time')
            plt.ylabel(f'{variables}')
            plt.title(f'{variables} Over Selected Time Range for {Sitename}')
            plt.xticks(rotation=0)
            plt.grid(True)
            print('0')
            plt.tight_layout()
            plt.savefig('static/Images/custom-analysis.png')

            plt.figure(figsize=(10, 5))
            plt.scatter(filtered_df.index, filtered_df[variables])
            plt.xlabel('Time')
            plt.ylabel(f'{variables}')
            plt.title(f'{variables} Over Selected Time Range  for {Sitename}')
            plt.xticks(rotation=0)
            plt.grid(True)
            plt.tight_layout()
            print('sving')
            plt.savefig('static/Images/scattercustom-analysis.png')
            plt.close()

            return redirect('displayanalysis')
        else:
            print('form not valid',form2.errors)
   
    else:
        form = AnayasisKpiForm()
        form2 = ServiceForm()
        Sitename = 'Nyama'
        
       
    content = {
        'form2': form2,
        'form': form,
        
      
    }

    return render(request, 'analysis.html', content)


@login_required(login_url='sign_in')
def Analysis_2(request):  
    print(request.user.city)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            print(request.user)
            
            start_time = request.POST.get('enddate', None)
            end_time = request.POST.get('startdate', None)
            df =  df_analysis[df_analysis['Begin Time'] >= start_time & (df_analysis['End Time'] <=  end_time)]
            variable = form.cleaned_data.get('Traffic')
            selection = form.cleaned_data.get('Service')
            tool = form.cleaned_data.get('Charts')
            df_selection = df[selection]
            df_variable = df[variable]
            if tool == 'bar':
                #bar graph
                plt.figure(figsize=(8, 5))  
                plt.bar(df_variable, df_selection)
                plt.xlabel(variable)
                plt.ylabel(selection)
                title = f'{variable} versus {selection}'
                plt.title(title)
                plt.xticks(rotation=45)  
            elif tool == 'Table':
                  # Line Graph
                plt.figure(figsize=(8, 5))
                plt.plot(df_variable, df_selection)  
                plt.xlabel(variable)
                plt.ylabel(selection)
                title = f'{variable} versus {selection}'
                plt.title(title)
                plt.xticks(rotation=45)
            elif tool == 'pie':
                # Pie Chart 
                plt.figure(figsize=(8, 5))
                plt.pie(df_variable.value_counts(), labels= df_variable.unique(), autopct="%1.1f%%",startangle=90) 
                plt.axis('equal') 
                plt.title(f"{selection} Distribution") 
           

        else:
            print('form not valid',form.errors)
   
    else:
        form = ServiceForm()
        Sitename = 'Nyama'
        
       
    content = {
       
        'form': form,
        
      
    }

    return render(request, 'analysis-2.html', content)

@login_required(login_url='sign_in')
def DisplayAnalysis(request):
  
    return render(request, 'displayanalysis.html')


@login_required(login_url='sign_in') 
def uploadDataSet(request):
    display = 'None'
    print(display)
    if request.method == 'POST':
        form = uploadDataForm(request.POST, request.FILES)
        print('in post')
        if form.is_valid():
            print('validating')
            display = 'block'
            print(display)
            dataset = form.save(commit=False)
            dataset.created_by = request.user
            if display == 'block':
                loading(request,dataset) 
            dataset.save()
            mesage= f'Dataset added succesfully'
            messages.success(request,mesage)
            return redirect('view_dataset')   
        else:
            messages.warning(request, form.errors)
    else:
        form = uploadDataForm()
        display = 'None'
    content = {}
    content = {
        'form': form,
        'display':display

    }
    return render(request, 'uploadDataSet.html', content)
def loading(request,dataset):
    dataset.save()
    return render(request ,'loading.html')

@login_required(login_url='sign_in') 
def uploadSiteNameData(request):
    if request.method == 'POST':
        form = uploadSiteForm(request.POST, request.FILES)
        if form.is_valid():
            display = 'block' 
            dataset = form.save(commit=False)
            dataset.created_by = request.user
            dataset.save()
            mesage= f'DataSite  added succesfully'
            messages.success(request,mesage)
           
            return redirect('dashboard')   
        else:
            messages.warning(request, form.errors)
    else:
        form = uploadSiteForm()
        display = 'None'
    content = {}
    content = {
        'form': form,
        'display':display

    }
    return render(request, 'uploadSite.html', content)


@login_required(login_url='sign_in') 
def CleaningPipeLine(request):
    content ={}
    content ={ 
    #'datasets':datasets
    }
   
    return render(request, 'view_dataset.html' ,content)

@login_required(login_url='sign_in') 
def viewDataSet(request):
    import pandas as pd
    #df = pd.read_excel(current.file)
   # rows , columns = df.shape

    content ={}
    content ={ 
    # 'datasets':datasets,
    # 'rows':rows,
    # 'cols':columns,
    # 'current':current
    }
   
    return render(request, 'view_dataset.html' ,content)



#-----------------------------------------------OBJECTIVE 5  COMMENTS-----------------------------------------------
#     5. To develop a system that allows Econet personel to add comments on KPI reports and
# helping them to make  data-driven decision
@login_required(login_url='sign_in') 
def finalComment(request):
    if request.method == 'POST':
        form =CommentForm(request.POST)
        print('validating the comment form')
        if form.is_valid():
            fm= form.save( commit=False)
            fm.created_by = request.user
            fm.save()
            print('form is saved')
           
            mgs = f'''
                You have succefully Added a {fm.types}'''
            messages.success(request, mgs)
            return redirect('dashboard')
        else:
            print('form not valid not valid')
            messages.warning(request, 'Form is not Valid')
    else:
        form =CommentForm()
    content = {}
    content = {
        'form': form
        
    }
    return render(request, 'add_commnet_report.html', content)
@login_required(login_url='sign_in') 
def Comments(request):
    content ={}
    content ={ 
    'comments':comments
    }
   
    return render(request, 'comments-reports.html' ,content)

@login_required(login_url='sign_in') 
def Final(request):
    content ={}
    content ={ 
    'finals':final
    }
   
    return render(request, 'final.html' ,content)





