from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm,UserCreationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from rest_framework.authtoken.models import Token
# Create your views here.
import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


def redirect_to_front(request):
    token = None
    if request.user.is_authenticated:
        token = Token.objects.create(user = request.user)
    response = redirect('http://localhost:3000/signin')
    response["Token"] = token if token else ""
    return response
def get_csrf(request):
    response = JsonResponse({"Info": "Success - Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response



def logout(request):
    auth.logout(request)
    print('user logged out')
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
            redirect_link=request.POST['next'] if 'next' in request.POST else "books"
            return redirect(redirect_link)
        else:   
            messages.info(request, 'Invalid Credentials')
            return redirect ( 'login')
    
 
    next=request.GET['next'] if 'next' in request.GET else "books"
    context['next']=next
    return render(request, 'ams/login.html',context)




# @csrf_exempt
# @require_POST
# def loginView(request):
#     data = json.loads(request.body)
#     username = data.get("username")
#     password = data.get("password")

#     if username is None or password is None:
#         return JsonResponse({"info": "Username and Password is needed"})

#     user = authenticate(username=username, password=password)

#     if user is None:
#         return JsonResponse({"info": "User does not exist"}, status=400)

#     login(request, user)
#     return JsonResponse({"info": "User logged in successfully"})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        print(request.user.is_staff)
        return JsonResponse({"username": request.user.username})

