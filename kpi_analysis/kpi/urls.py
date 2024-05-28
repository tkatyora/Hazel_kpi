from django.urls import path
from . import views

urlpatterns = [
    path('',views.signIn, name = 'sign_in'),
    path('logout',views.signout , name ='logout'),  
    path('dashboard',views.dashboard, name = 'dashboard'),
    path('addUser',views.addNewUser, name = 'add_user'),
    path('change_password',views.ChangePassword, name='change_passorword'),
    path('view_user',views.viewUser, name = 'view_user'),path('view_user',views.viewUser, name = 'view_user'),
    path('delete_user/<int:pk>', views.deleteUser,name ='delete_user'),
    path('add_Comment',views.finalComment, name = 'add_comment'),
    path('analysis',views.Analysis, name = 'analysis'),
    path('displayanalysis',views.DisplayAnalysis, name = 'displayanalysis'),
    path('analysis_variable',views.AnalysisVariable, name = 'analysis_variable'),
    path('upload_dataset',views.uploadDataSet, name = 'upload_dataset'),
    path('upload_sitename',views.uploadSiteNameData, name = 'upload_sitename'),
    path('view_dataset',views.viewDataSet, name = 'view_dataset'),
    path('comments',views.Comments, name = 'comments'),
    path('Final_Decision',views.Final, name = 'final'),
    path('whole_analysis',views.WholeAnalysis, name = 'wholeanalysis'),
    path('loading',views.loading, name = 'loading'),
]
