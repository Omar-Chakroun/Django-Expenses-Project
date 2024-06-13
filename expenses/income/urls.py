from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="incomes"),
    path('add-income', views.add_income, name="add-incomes"),
    path('edit-inc/<int:id>', views.edit_income, name="edit-incomes"),
    path('delete-income/<int:id>', views.delete_income, name="delete-incomes"),
    path('search-incomes', csrf_exempt(views.search_income), name="Search-incomes"),
    path('incomes-by-category/', views.incomes_by_category, name='incomes-by-category'),
    path('incomes-summary/incomes-by-category/', views.incomes_by_category, name='incomes-by-category'),
    path('incomes-summary/', views.incomes_summary, name='incomes-summary'),
    path('incomes-summary/incomes-by-category-today/', views.incomes_by_category_today, name='incomes-by-category-today'),
    path('incomes-summary/incomes-by-category-month/', views.incomes_by_category_month, name='incomes-by-category-month'),
    path('incomes-summary/incomes-by-category-year/', views.incomes_by_category_year, name='incomes-by-category-year')
]
