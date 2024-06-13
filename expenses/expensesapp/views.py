from django.shortcuts import render,redirect
from django.http import request,JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
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
    expenses=Expense.objects.filter(owner=request.user)
    paginator=Paginator(expenses,5)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    currency=UserPref.objects.get(user=request.user).currency
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
             }
    return render(request,'expenses/index.html',context)

@login_required(login_url="/authentication/login/")
def add_exp(request):
    categories=Category.objects.all()
    context={
            'categories':categories
        }
    if request.method=='GET':
        return render(request,'expenses/add_exp.html',context)

    if request.method =='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        dates=request.POST['date']
        category=request.POST['category']
        if not amount:
            messages.error(request,'Please enter the amount !')
            return render(request,'expenses/add_exp.html',context)
        if not description:
            messages.error(request,'Please enter a description !')
            return render(request,'expenses/add_exp.html',context)
        Expense.objects.create(owner=request.user,amount=amount,date=dates,category=category,description=description)
        messages.success(request,'Expense saved successfuly!')
        return redirect('expenses')
    
@login_required(login_url="/authentication/login/")
def expense_edit(request,id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()

    if request.method=='GET':
        context={
            'expense':expense,
            'values':expense,
            'categories':categories}
        return render(request,'expenses/edit-expense.html',context)
    if request.method=='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        dates=request.POST['date']
        category=request.POST['category']
        if not amount:
            messages.error(request,'Please enter the amount !')
            return render(request,'expenses/edit-expense.html',context)
        if not description:
            messages.error(request,'Please enter a description !')
            return render(request,'expenses/edit-expense.html',context)
        
        expense.owner=request.user
        expense.description=description
        expense.date=dates
        expense.category=category
        expense.amount=amount
        expense.save()
        messages.success(request,'Expense has been updated successfuly!')
        return redirect('expenses')
    
@login_required(login_url="/authentication/login/")    
def delete_expenses(request,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense removed')
    return redirect('expenses')
    
@login_required(login_url="/authentication/login/")    
def search_expenses(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        
        expenses = Expense.objects.filter(
            Q(amount__istartswith=search_str,owner=request.user) |
            Q(description__icontains=search_str,owner=request.user) |
            Q(category__icontains=search_str,owner=request.user)  |
            Q(date__istartswith=search_str,owner=request.user)
            
        )
        data=expenses.values()
        return JsonResponse(list(data),safe=False)
    




@login_required(login_url="/authentication/login/")
def expenses_by_category(request):
    if request.method == 'GET':
        today = date.today()
        six_months_ago=today-relativedelta(months=6)
        year_ago=today-relativedelta(months=12)
        expenses = Expense.objects.filter(owner=request.user).values('category').annotate(total_amount=Sum('amount'))
        today_amount=Expense.objects.filter(owner=request.user,date=today).aggregate(total_amount=Sum('amount'))
        month_amount=Expense.objects.filter(owner=request.user,date__range=[six_months_ago,today]).aggregate(total_amount=Sum('amount'))
        year_amount=Expense.objects.filter(owner=request.user,date__range=[year_ago,today]).aggregate(total_amount=Sum('amount'))
        
        data = list(expenses)
        response_data={
            'data':data,
            'amount':today_amount,
            'month_amount':month_amount,
            'year_amount':year_amount

        }
        return JsonResponse(response_data, safe=False)

@login_required(login_url="/authentication/login/")
def expenses_by_category_today(request):
    if request.method == 'GET':
        today = date.today().strftime("%Y-%m-%d")
        expenses = Expense.objects.filter(owner=request.user, date=today).values('category').annotate(total_amount=Sum('amount'))
        new_data = list(expenses)
        return JsonResponse(new_data, safe=False)

@login_required(login_url="/authentication/login/")
def expenses_by_category_month(request):
    if request.method == 'GET':
        today = date.today()
        six_months_ago=today-relativedelta(months=6)
        expenses = Expense.objects.filter(owner=request.user, date__range=[six_months_ago,today]).values('category').annotate(total_amount=Sum('amount'))
        new_data_month = list(expenses)
        return JsonResponse(new_data_month, safe=False)

@login_required(login_url="/authentication/login/")
def expenses_by_category_year(request):
    if request.method == 'GET':
        today = date.today()
        year_ago=today-relativedelta(months=12)
        expenses = Expense.objects.filter(owner=request.user, date__range=[year_ago,today]).values('category').annotate(total_amount=Sum('amount'))
        new_data_year = list(expenses)
        return JsonResponse(new_data_year, safe=False)



@login_required(login_url="/authentication/login/")
def expenses_summary(request):
    expenses=Expense.objects.filter(owner=request.user)
    context={
        'expenses':expenses
    }
    return render(request,'expenses/sumary_expenses.html',context)


@login_required(login_url="/authentication/login/")
def export_csv(request):

    response=HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses=Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])
    return response
        
@login_required(login_url="/authentication/login/")
def export_pdf  (request):

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"data_{current_time}.xlsx"

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Data'

    headers = ['Amount','Description','Category','Date']
    worksheet.append(headers)

    # Add the data
    for expense in Expense.objects.all():
        row = [expense.amount,expense.description,expense.category,expense.date]
        worksheet.append(row)

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
 
    workbook.save(response)

    return response
