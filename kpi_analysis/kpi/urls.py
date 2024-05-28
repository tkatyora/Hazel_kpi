from django.urls import path
from . import views

urlpatterns = [
    path('',views.signIn, name = 'sign_in'),
    path('logout',views.signout , name ='logout'),  
    path('dashboard',views.dashboard, name = 'dashboard'),
    path('addUser',views.addNewUser, name = 'add_user'),
    path('change_password',views.ChangePassword, name='change_passorword'),
    path('view_user',views.viewUser, name = 'view_user'),path('view_user',views.viewUser, name = 'view_user'),
    path('delete-user/<int:pk>', views.deleteUser,name ='delete_user'),
    path('add-Comment',views.finalComment, name = 'add_comment'),
    path('analysis',views.Analysis, name = 'analysis'),
    path('displayanalysis',views.DisplayAnalysis, name = 'displayanalysis'),
    path('analysis-variable',views.AnalysisVariable, name = 'analysis_variable'),
    path('upload-dataset',views.uploadDataSet, name = 'upload_dataset'),
    path('upload-sitename',views.uploadSiteNameData, name = 'upload_sitename'),
    path('view-dataset',views.viewDataSet, name = 'view_dataset'),
    path('comments',views.Comments, name = 'comments'),
    path('Final-Decision',views.Final, name = 'final'),
    path('whole-analysis',views.WholeAnalysis, name = 'wholeanalysis'),
    path('loading',views.loading, name = 'loading'),
]
