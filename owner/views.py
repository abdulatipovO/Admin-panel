from django.shortcuts import render, redirect
from django.views import View
from .tools import *
from main.models import *


# Create your views here.


class HomeView(View):
    def get(self, request):

        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        service = Service.objects.filter(owner=request.user)
        context ={
            'category':category,
            'weekday' :weekday,
            'service':service

        }

        return render(request,'index.html', context)


class LoginView(View):
    def get(self, request):
        return render(request,'login.html')

    def post(self, request):
        login = login_(request)
        if login:
            return redirect('/')
        print('xato login view')
        return render(request,'login.html')

def logout_(request):
    logout(request)
    return redirect('owner:login')

class RegisterView(View):
    def get(self, request):
        return render(request,'register.html')

    def post(self, request):
        register = register_(request)
        if register:
            return redirect('/verification')
        print('xato')
        return render(request,'register.html')

class VerificationView(View):
    def get(self, request):
        return render(request,'verification.html')

    def post(self, request):
        v = checkVerification(request)
        if v:
            return redirect('/')
        return render(request,'verification.html')

class IntroView(View):
    def get(self,request):
        return render(request,'intro.html')


class ServiceView(View):
    

    def post(self,request):
        service =  service_register(request)
        if service == True:
            return redirect('/')
        return redirect('/')
