from django.shortcuts import redirect, render
from django.views import View
from pymongo import collection
from . import forms
from django.contrib.auth.models import auth,User
from django.contrib import messages 
import dbinfo



class Home(View):
    def get(self,request):
        collection = dbinfo.database['data']
        user_data = collection.find_one({'user_id' : request.user.username})
        content = {
            'page_title' : 'Homepage',
            'task_form' : forms.TodoForm(),
            'todo_list' : user_data['todo_list']
        }
        return render(request,'index.html',content)


class LoginUser(View):
    def get(self,request):
        content ={
            'page_title' : 'LoginPage',
            'login_form' : forms.LoginForm()
        }
        return render(request,'login_page.html',content)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username , password=password)
        if user is not None:
            print('yes')
            auth.login(request,user)
            messages.success(request,"Login successfully")
        return redirect('/')

class SignupUser(View):
    def get(self,request):
        content = {
            'page_title' : 'Sign up',
            'signup_form' : forms.SignupForm()
        }
        return render(request,'signup.html',content)

    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        collection = dbinfo.database['data']

        new_user = User.objects.create_user(username=username , email=email, password=password)
        new_user.save()
        user_data = {
            'user_id' : username,
            'todo_list' : []
        }
        collection.insert(user_data)
        messages.success(request,"Signup successfully")
        return redirect('/login')



class Logout(View):
    def get(self,request):
        auth.logout(request)
        return redirect('/')



class NewTask(View):
    def post(self,request):
        collection = dbinfo.database['data']
        todo_list = collection.find_one({'user_id' : request.user.username})
        data_to_add = request.POST['task']
        old_data = todo_list['todo_list']
        new_data = []
        new_data.append(data_to_add)
        new_data = new_data + old_data

        collection.update_one(
            
            {
                'user_id':request.user.username
            },
            {
                '$set':{
                    'todo_list':new_data
                }
            },
            upsert=False,
        )

        messages.success(request,"Task Added Successfully")
        return redirect('/')


class DeleteTask(View):
    def post(self,request):
        collection = dbinfo.database['data']
        user_data = collection.find_one({'user_id' : request.user.username })
        old_data = user_data['todo_list']
        task = request.POST['task']
        old_data.remove(task)

        collection.update_one(
            {
                'user_id' : request.user.username
            },
            {
                '$set' : {
                    'todo_list' : old_data
                }

            },
            upsert = False
        )

        messages.success(request,"Task deleted successfully")

        return redirect('/')