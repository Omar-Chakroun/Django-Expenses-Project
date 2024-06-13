from django.shortcuts import render
import json 
import os
from django.conf import settings
from .models import UserPref
from django.contrib import messages
# Create your views here.

def index(request):

    currency_data=[]
    file_path=os.path.join(settings.BASE_DIR,'currencies.json')
    with open(file_path,'r') as json_file:
        data=json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name': k ,'value': v})

    perf_exists=UserPref.objects.filter(user=request.user).exists()
    user_perferences=None
    if perf_exists:
        user_perferences=UserPref.objects.get(user=request.user)
    if request.method=="GET":



        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_perferences': user_perferences})

    else:
        currency=request.POST['currency']
        if perf_exists:
            user_perferences.currency=currency
            user_perferences.save()
        else:

            UserPref.objects.create(user=request.user,currency=currency)
        messages.success(request,"perference saved !")
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_perferences': user_perferences})

