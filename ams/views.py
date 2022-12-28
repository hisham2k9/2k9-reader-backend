from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm,UserCreationForm
from django.contrib.admin.forms import AdminAuthenticationForm
# Create your views here.




def logout(request):
    auth.logout(request)
    return redirect( 'login')

def login(request):
    context={}
    context['loginform']=AdminAuthenticationForm()
    
    if request.method=='POST':
        username = request.POST['username']
        password= request.POST['password']
        user = auth.authenticate(request,username=username, password=password)
        if user is not None:
            auth.login(request, user)
            redirect_link=request.POST['next'] if 'next' in request.POST else "home"
            return redirect(redirect_link)
        else:   
            messages.info(request, 'Invalid Credentials')
            return redirect ( 'login')
    
 
    next=request.GET['next'] if 'next' in request.GET else "home"
    context['next']=next
    return render(request, 'ams/login.html',context)
