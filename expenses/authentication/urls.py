from django.urls import path
from .views import ResgisterView,UsernameValidation,EmailValidation,VerficationView,LoginView,LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('validate-username',csrf_exempt(UsernameValidation.as_view()),name="validate_name"),
    path('register/',ResgisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('validate-email',csrf_exempt(EmailValidation.as_view()),name="validate_email"),
    path('activate/<uidb64>/<token>',VerficationView.as_view(),name="activate")
]
