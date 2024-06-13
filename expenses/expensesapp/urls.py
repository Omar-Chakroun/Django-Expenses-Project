from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
path('',views.index,name="expenses"),
path('add-exp',views.add_exp,name="add-expenses"),
path('edit-exp/<int:id>',views.expense_edit,name="edit-expenses"),
path('delete-exp/<int:id>',views.delete_expenses,name="delete-expenses"),
path('search-expenses',csrf_exempt(views.search_expenses),name="search-expenses"),
path('expenses-by-category/', views.expenses_by_category, name='expenses-by-category'),
path('expenses-summary/expenses-by-category-today/', views.expenses_by_category_today, name='expenses-by-category-today'),
path('expenses-summary/expenses-by-category-month/', views.expenses_by_category_month, name='expenses-by-category-month'),
path('expenses-summary/expenses-by_category-year/', views.expenses_by_category_year, name='expenses-by-category-year'),
path('expenses-summary/', views.expenses_summary, name='expenses-summary'),
path('export-csv/', views.export_csv, name='export-csv'),
path('export-pdf/', views.export_pdf, name='export-pdf')

]