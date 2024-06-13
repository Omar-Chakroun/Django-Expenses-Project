from django.shortcuts import render,redirect
from django.http import request,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Source,UserIncome
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.db.models import Q
from userpreferences.models import UserPref
from django.db.models import Sum
import csv,openpyxl
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
# Create your views here.


@login_required(login_url="/authentication/login/")
def index(request):
    incomes=UserIncome.objects.filter(owner=request.user)
    paginator=Paginator(incomes,5)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPref.objects.get(user=request.user).currency
    context={
        'incomes':incomes,
        'page_obj':page_obj,
        'currency':currency
             }
    return render(request,'income/index.html',context)



@login_required(login_url="/authentication/login/")
def add_income(request):
    Sources=Source.objects.all()
    context={
            'sources':Sources
        }
    if request.method=='GET':
        return render(request,'income/add_inc.html',context)

    if request.method =='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        dates=request.POST['date']
        source=request.POST['source']
        if not amount:
            messages.error(request,'Please enter the amount !')
            return render(request,'income/add_inc.html',context)
        if not description:
            messages.error(request,'Please enter a description !')
            return render(request,'income/add_inc.html',context)
        UserIncome.objects.create(owner=request.user,amount=amount,date=dates,source=source,description=description)
        messages.success(request,'Expense saved successfuly!')
        return redirect('incomes')

@login_required(login_url="/authentication/login/")
def edit_income(request,id):
    sources=Source.objects.all()
    income=UserIncome.objects.get(pk=id)
    
    if request.method=='GET':
        context={
            'incomes':income,
            'sources':sources,
            'values':income
        }
        return render(request,'income/edit_inc.html',context)

    if request.method =='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        dates=request.POST['date']
        source=request.POST['source']
        if not amount:
            messages.error(request,'Please enter the amount !')
            return render(request,'income/add_inc.html',context)
        if not description:
            messages.error(request,'Please enter a description !')
            return render(request,'income/add_inc.html',context)
        

        income.owner=request.user
        income.description=description
        income.date=dates
        income.source=source
        income.amount=amount
        income.save()
        messages.success(request,'Income has been updated successfuly!')
        return redirect('incomes')
    
@login_required(login_url="/authentication/login/")
def delete_income(request,id):
    income=UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,'Income removed')
    return redirect('incomes')


@login_required(login_url="/authentication/login/")
def search_income(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        incomes=UserIncome.objects.filter(
            Q(amount__istartswith=search_str,owner=request.user) |
            Q(description__icontains=search_str,owner=request.user) |
            Q(source__icontains=search_str,owner=request.user)  |
            Q(date__istartswith=search_str,owner=request.user)
        )
        data=incomes.values()
        return JsonResponse(list(data),safe=False)
    




@login_required(login_url="/authentication/login/")
def incomes_by_category(request):
    if request.method=='GET':
        incomes=UserIncome.objects.filter(owner=request.user).values('source').annotate(total_amount=Sum('amount'))
        data=list(incomes)
        return JsonResponse(data, safe=False)



@login_required(login_url="/authentication/login/")
def incomes_summary(request):
    incomes=UserIncome.objects.filter(owner=request.user)
    context={
        'incomes':incomes
    }
    return render(request,'income/sumary_income.html',context)


@login_required(login_url="/authentication/login/")
def incomes_by_category_today(request):
    if request.method=='GET':
        today = date.today().strftime("%Y-%m-%d")
        incomes=UserIncome.objects.filter(owner=request.user,date=today).values('source').annotate(total_amount=Sum('amount'))
        new_data=list(incomes)
        
        return JsonResponse(new_data,safe=False)


@login_required(login_url="/authentication/login/")
def incomes_by_category_month(request):
    if request.method=='GET':
        today=date.today()
        six_months_ago=today-relativedelta(months=6)
        incomes=UserIncome.objects.filter(owner=request.user, date__range=[six_months_ago,today]).values('source').annotate(total_amount=Sum('amount'))
        new_data_month=list(incomes)
        return JsonResponse(new_data_month,safe=False)

@login_required(login_url="/authentication/login/")
def incomes_by_category_year(request):
    if request.method=='GET':
        today=date.today()
        year=today-relativedelta(months=12)
        incomes=UserIncome.objects.filter(owner=request.user, date__range=[year,today]).values('source').annotate(total_amount=Sum('amount'))
        new_data_year=list(incomes)
        return JsonResponse(new_data_year,safe=False)