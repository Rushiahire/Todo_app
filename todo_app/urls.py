from django.urls import path
from . import views


urlpatterns = [
    path("",views.Home.as_view(),name='home'),
    path('login',views.LoginUser.as_view(),name='login'),
    path('signup',views.SignupUser.as_view(),name='signup'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('new_task',views.NewTask.as_view(),name='newtask'),
    path('delete',views.DeleteTask.as_view(),name='deletetask')
]
