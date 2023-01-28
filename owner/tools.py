from main.models import * 
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from customer.utils import CreateVerificationCode
from django.contrib import messages



def register_(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    phone = request.POST['phone']
    address= request.POST['address']
    password1= request.POST['password1']
    password2= request.POST['password2']

    if len(password1) < 8:
        print('parol 8 tadan kam bolmasligi kerak')
        # "password must be less than 8 characters"
        messages.error(request, "Parol 8 ta belgidan kam bo'lmasligi kerak !")
        return False

    if password1 != password2:
        print('parollar bir xil emas')
        # "Passwords is not equal"
        messages.error(request, "Parollar bir xil emas !")
        return False

    try:
        verification_code = CreateVerificationCode()
        user = User.objects.get(phone=phone)
        if user.is_active == False:
            user.verification_code=verification_code

            #send code
            print(f'{verification_code} kod yuborildi(try)')
        else:
            messages.error(request, "Siz oldin ro'yxatdan o'tgansiz !")
            return False
        request.session['phone'] = phone
        user.save()
        return True
    except:
        if User.objects.filter(username=username).exists():
            # "This username already exists"
            messages.error(request, "Bu username oldin ro'yxatdan o'tgan !")

            return False

        if User.objects.filter(phone=phone).exists():
            # "This phone already exists"
            messages.error(request, "Bu telefon raqam oldin ro'yxatdan o'tgan !")

            return False
        else:
            verification_code = CreateVerificationCode()
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                adres=address,
                password=password1,
                verification_code=verification_code,
                is_active=False,
            )
            request.session['phone'] = phone
            print(f'{verification_code} kod yuborildi(except)')

        return True


def login_(request):
    username = request.POST['username']
    password = request.POST['password']

    if username and password:
            try:
                # user =  User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    return True
            except:
                return False
    messages.error(request, "Login yoki parol xato !")


def checkVerification(request):
    phone = request.session['phone']
    ver_code = request.POST['ver_code']
    user = User.objects.filter(phone=phone)[0]
    if ver_code == user.verification_code:
        user.is_active =True
        user.save()
        return True
    messages.error(request, "Tasdiqlash kodi noto'g'ri kiritildi !")
    return False


def service_register(request):
    user = request.user
    user = User.objects.filter(username=user.username)[0]
    name = request.POST['name']
    adres = request.POST['adres']
    description = request.POST['description']
    img = request.POST['img']
    category = request.POST['category']
    category = Category.objects.filter(name=category)[0]
    phone = request.POST['phone']
    phone_2 = request.POST['phone_2']
    working_time_from = request.POST['working_time_from']
    working_time_to = request.POST['working_time_to']
    working_days = request.POST['working_days']
    working_day = WeekDay.objects.filter(day_name=working_days)[0]
    open_service = request.POST['open_service']
    open_service = True if open_service == '1' else False
    service = Service.objects.create(owner=user,
                                        name=name,
                                        adres=adres,
                                        description=description,
                                        image = img,
                                        category=category,
                                        phone=phone,
                                        phone_2=phone_2,
                                        working_time_from=working_time_from,
                                        working_time_to=working_time_to,
                                        open_service=open_service)

    service.working_days.add(working_day)
    # service = messages.error(request, " hatolik yuzberdi ")  if service  else messages.error(request, " hatolik yuzberdi ")
    service = True if service  else False
    return service