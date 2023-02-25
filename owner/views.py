from django.shortcuts import render, redirect
from django.views import View
from .tools import *
from main.models import *
from .decorators import deco_login
import datetime
from django.http import JsonResponse



# Create your views here.

today = datetime.datetime.now()
class HomeView(View):
    @deco_login
    def get(self, request):
        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        context ={
            'category':category,
            'weekday' :weekday,
        }
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
            "today":today.date
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
      
        update = room_update(request,pk)
        if update:
            return redirect(f"/room/update/{pk}")
        img  =  img_create(request,pk)
        if img:
            return redirect(f"/room/update/{pk}")
        print("xatooooo")
        return redirect(f"/room/update/{pk}")

class BronView(View):
    def get(self,request, pk):
        service = Service.objects.get(pk=pk)
        return render(request, 'fullcalendar.html', {"service":service})
    
def calendar_view(request, pk):
    rooms = Room.objects.filter(service=pk)
    events = []
    for r in rooms:
        brons = Bron.objects.filter(room=r.id)
        for bron in brons:
            f = bron.time_from.strftime("%H:%M")
            e = bron.time_to.strftime("%H:%M")
            event = {
                'id': r.id,
                'title': f'{ f } dan { e } gacha',
                'start': f"{bron.date}T{bron.time_from}",
                'end': f"{bron.date}T{bron.time_to}",
                'className': 'success',
                'allDay': False,
            }
            events.append(event)
        
    data  = {
        "data":events
    }
    return JsonResponse(data)


def infoBrons(request):
    pk = request.GET['pk']
    day = request.GET['day']
    month = request.GET['month']
    year = request.GET['year']
    print(month)
    print(month)
    print(month)
    date = datetime.date(int(year),int(month),int(day))
    print(date)
    
    service = Service.objects.get(id=pk)
    rooms = Room.objects.filter(service=service)
    bron = Bron.objects.filter(date=date)
    d = {}
    for r in rooms:
        bron = Bron.objects.filter(date=date)
       
        for b in bron:
            
            d[f'{r.id}'] = {
                "title":f"{b.time_from} dan {b.time_to} gacha"
            }
    print(bron)
    
    return JsonResponse({"status":"ok", "brons":d })
    
    
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
            messages.success(request, "Xona muvaffaqiyatli band qilindi !")
        else:
            for i in bron:
                messages.error(request, f"Ushbu xona {i.date} kuni {str(i.time_from)[:5]} dan {str(i.time_to)[:5]} gacha band !")
        room =  Room.objects.filter(service=pk)
        context = {
            "rooms":room,
            "pk":pk
        }

        return render(request, 'add_bron.html', context)
    
class BronCancelView(View):
    def post(self, request):
        service_id = int(request.POST['id_service'])
        cancelBron(request)
        return redirect(f'/service/{service_id}')


class OwnerProfilView(View):
    @deco_login
    def get(self, request):
        user = User.objects.filter(username=request.user)[0]
        return render(request, 'owner_profil.html',{"user":user})
    
    def post(self, request):
        profilUpdate(request)
        return redirect('/profil')
    
    
 
