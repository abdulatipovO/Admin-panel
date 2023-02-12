from django.shortcuts import render, redirect
from django.views import View
from .tools import *
from main.models import *
from .decorators import deco_login
import datetime
        


# Create your views here.


class HomeView(View):
    @deco_login
    def get(self, request):
        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        context ={
            'category':category,
            'weekday' :weekday,
        }
        # WeekDay.objects.create(day_name='haftada 7 kun',day_number=7)
        # Category.objects.create(name='samavor')
        try:
            service = Service.objects.filter(owner=request.user)
            context['service'] = service
        except:
            pass
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

class ServiceDetailView(View):
    @deco_login
    def get(self, request,pk):
        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        service = Service.objects.get(id=pk)
        rooms = Room.objects.filter(service=service)
        context = {
            'category':category,
            'weekday':weekday,
            'service':service,
            'rooms':rooms,
        }
        return render(request,'detail_service.html', context)
    def post(self, request,pk):
        service =  service_update(request,pk)
        if service == True:
            return redirect(f'/service/{pk}')
        return redirect('/')


class RoomView(View):
    def post(self,request ,pk):
        room  = room_create(request ,pk)
        if room == True:
            return redirect(f'/service/{pk}')
        return redirect(f'/service/{pk}')



class RoomUpdateView(View):
    @deco_login
    def get(self,request,pk):
        room = Room.objects.get(id=int(pk))
        # image = room.room_photos.all()
        context = {'room':room,
                   }
        return render(request,'room_parametr.html',context)
    def post(self,request,pk):
        print(pk)
        print(pk)
        print(pk)
        update = room_update(request,pk)
        if update:
            return redirect(f"/room/update/{pk}")
        img  =  img_create(request,pk)
        if img:
            return redirect(f"/room/update/{pk}")
        print("xatooooo")
        return redirect(f"/room/update/{pk}")

class BronView(View):
    @deco_login
    def get(self,request,pk ):
        today = datetime.date.today()
        rooms = Room.objects.filter(service=pk)
        print(rooms)
        l = []
        for r in rooms:
            bron = Bron.objects.filter(room=r.id).filter(date__gte=today)
            l.append(bron)

        context  = {
            "brons":l
        }

        return render(request, 'bron_list.html', context)

class BronAddView(View):
    def get(self, request,pk):
        room =  Room.objects.filter(service=pk)
        context = {
            "rooms":room,
            "pk":pk
        }
        return render(request, 'add_bron.html', context)

    def post(self, request,pk):

        bron = addBron(request,pk)
        if bron == True:
            print("create")
            return redirect('/')
        print(bron, 'bu listda shu kungi barcha bronlar bor ')  # message yoki biror sahifaga jonatib belgi berish kerak 
        return redirect('/')