from django.http import request
from django.views import View
from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail

from django.utils.encoding import force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
class ResgisterView(View):
    def get(self,request):
        return render(request,'auth/register.html')
    

    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']  
        password = request.POST['password']
        
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if 'password' not in request.POST or not request.POST['password']:
                    messages.error(request, 'Password field is empty')
                    return render(request, 'auth/register.html')
                
                if len(password)<6 : 
                    messages.error(request,'Password too short ')
                    return render(request,'auth/register.html')
                
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=False 
                user.save()
                current_site = get_current_site(request)
                messages.success(request,"User created successfully")
                

                uidb64 = urlsafe_base64_encode(str(user.pk).encode())

                
                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                
                activate_url='http://'+current_site.domain+link
                email_body='Hello '+user.username+' Use this link to activate your account :\n'+activate_url
                send_mail(
                    "Subject here",
                    email_body,
                    "from@example.com",
                    [email],
                    fail_silently=False,
                )                    
        return render(request,"auth/register.html")



class UsernameValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data.get('username')
        if not str(username).isalnum():
            return JsonResponse( {'username_error':'Username should  containt only alphanumeric caracters'},status=400,safe=False)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username already exists!'},status=409,safe=False)
        
        
        return JsonResponse({'username_valid':True})
    
class EmailValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data.get('email')
        if not validate_email(email):
            return JsonResponse( {'email_error':'email not valid'},status=400,safe=False)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email already exists!'},status=409,safe=False)
        
        
        return JsonResponse({'email_valid':True})

class VerficationView(View):
    def get(self,request,uidb64,token):
        
        try :
            id=force_str(urlsafe_base64_decode(uidb64)) 
            user=User.objects.get(pk=id)

            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request,'Account activated successfuly')
            redirect('login')

        except Exception as exp:
            pass


        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'auth/login.html')
    

    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    return redirect('expenses')
                
                messages.error(request,'Account is not active')
                return render(request,'auth/login.html')
            
            messages.error(request,'Invalid credentials')
            return render(request,'auth/login.html')
        
        messages.error(request,'Please fill the fields')
        return render(request,'auth/login.html')
    

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')