from django.urls import path
from .views import index,edit_profile
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',index,name="edit_profile"),
    path('edit/',edit_profile,name="edit")
]
