from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.mail import send_mail
from .form import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
import threading
from django.conf import settings


# VARIABLES
users = User.objects.all()
latest_dataset = DataSet.objects.latest('created_on')  
datasets = DataSet.objects.exclude(pk=latest_dataset.pk).order_by('-created_on')
# datasets = DataSet.objects.all().order_by('-created_on')
current = DataSet.objects.latest('created_on') 
anaysis_dataset = DataSet.objects.last()
comments = CommentReports.objects.all()
final = CommentReports.objects.filter(types='finaldecision').order_by('-created_on').first()

#------------------------------------------Function for sending email----------------------------
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

#---------------------------OBJECTIVE 1 [USER AUTHENTICATION AND VALIDATION]------------------------------
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
            messages.warning(request, 'Invalid Username or  Paasword')
            return redirect('sign_in')
                      
    return render(request, 'sign_in.html' )

@login_required(login_url='sign_in') 
def addNewUser(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            print('The Regestration Function Excuted') 
            email = user_form.cleaned_data.get('email',None)
            name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            cities = user_form.cleaned_data.get('city')
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
            #user.city.set(cities) 
            user.save()
            msg = f'''
                Weclome  {name.title()} {last_name.title() }  to Econet KPI Anaysis Systsem

                Use the following credintials to log in into the system

                Domain Name : {username}
                password :{password}


                Econet inspired to change your word
                    '''
            email = EmailMessage(subject='Econet KPI Anaysis System', body=msg,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[email]
                         )
    
            #EmailThread(email).start()
            msg2 = f'{name} {last_name} is added Succefully with username {username}'
            messages.success(request, msg2)
            print('email sent ')
            print(send_mail)
            return redirect('dashboard')
            
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


#--- OBJECTIVE 4 CUSTOMIZABLE ANALYTICS AND VISUALIZATION ----------------------------------------
@login_required(login_url='sign_in')
def Analysis(request):
    print(request.method)
    if request.method == 'POST':
        import pandas as pd
        import matplotlib.pyplot as plt
        print('post')
        form = AnayasisKpiForm(request.POST)
        # Read the DataFrame
        if anaysis_dataset.types == 'csv':
            print('in csv')
            #df_predict = pd.read_csv('media/dataset.csv')
            a = 10
        elif anaysis_dataset.types == 'xlsx':
            df_predict = pd.read_excel('media/QualityOfCare.xlsx')
            a = 20
        else:
            print('Wrong format selected')
            a = 18
        date = request.POST.get('date', None)
        starttime = request.POST.get('starttime', None)
        endtime = request.POST.get('endtime', None)
        user_city = request.user.city
        if form.is_valid():
            variable = form.cleaned_data.get('variable')
            print(variable)
        else:
            print('form not valid',form.errors)
        # Filter the DataFrame for specific customer and time range
        # df_display = df_predict[(df_predict['Date'] == date)]
        # df_predict = df_display[(df_display['Time'] >= starttime) & (df_display['Time'] <= endtime)]
        # df_customer = df_predict[df_predict['Destination.IP'] == ip]

        # # Create subplots
        # fig, axs = plt.subplots(2, 1, figsize=(10, 10))

        # # Plot DownUp Ratio
        # axs[0].plot(df_customer['Time'], df_customer['Down.Up.Ratio'])
        # axs[0].set_title('Graph for Down Up Ratio')
        # axs[0].set_xlabel('Time')
        # axs[0].set_ylabel('DownUp Ratio')
        # axs[0].tick_params(axis='x', rotation=85)

        # # Plot ACK
        # axs[1].plot(df_customer['Time'], df_customer['ACK.Flag.Count'])
        # axs[1].set_title('ACKAcknowledgement Graph')
        # axs[1].set_xlabel('Time')
        # axs[1].set_ylabel('Acknowledgement Flag')
        # axs[1].tick_params(axis='x', rotation=85)
        # plt.tight_layout()
        # # Save figures
        # plt.savefig('static/Images/Prediction/updowns_ack.png')
        # plt.close()
       
    else:
        form = AnayasisKpiForm()
        variable = 'variable'
        user_city= 'city'
        date ='date'
        starttime = 'starttime'
        endtime ='endtime'
        print('get')

   
    content = {
        'variable': variable,
        'city': user_city,
        'date': date,
        'starttime': starttime,
        'endtime': endtime,
        'form': form

    }

    return render(request, 'analysis.html', content)

@login_required(login_url='sign_in') 
def AnalysisVariable(request):
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
         add_varible_form = AnayasisVariablesForm()

    content ={}
    content ={ 
    'form':analysis_form,
    'form2':add_varible_form
    }
   
    return render(request, 'variable.html' ,content)




#-----------------------------------------DASHBOARD---------------------------------------------
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


#-------------------------------------------USER MANAGAEMENT-------------------------------------


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

#-----------------------------------------------COMMENTS-----------------------------------------------
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
#-------------------------------------------------------------------DATASETS---------------------------------------

@login_required(login_url='sign_in') 
def uploadDataSet(request):
    if request.method == 'POST':
        form = uploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.created_by = request.user
            dataset.save()
            mesage= f'Dataset added succesfully'
            messages.success(request,mesage)
            return redirect('view_dataset')   
        else:
            messages.warning(request, form.errors)
    else:
        form = uploadDataForm()
    content = {}
    content = {
        'form': form,

    }
    return render(request, 'uploadDataSet.html', content)


@login_required(login_url='sign_in') 
def CleaningPipeLine(request):
    content ={}
    content ={ 
    'datasets':datasets
    }
   
    return render(request, 'view_dataset.html' ,content)



@login_required(login_url='sign_in') 
def viewDataSet(request):
    import pandas as pd
    df = pd.read_excel(current.file)
    rows , columns = df.shape

    content ={}
    content ={ 
    'datasets':datasets,
    'rows':rows,
    'cols':columns,
    'current':current
    }
   
    return render(request, 'view_dataset.html' ,content)

#----------------------------Commets------------------------------

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