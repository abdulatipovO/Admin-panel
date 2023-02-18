from django.urls import path
from .views import *



app_name = 'owner'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout_, name='log_out'),
    path('intro', IntroView.as_view(), name='intro'),
    path('verification', VerificationView.as_view(), name='verification'),
    path('service' , ServiceView.as_view(),name = 'service'),
    path('service/<int:pk>' , ServiceDetailView.as_view(),name = 'service_detail'),
    path('room_create/<int:pk>' , RoomView.as_view(),name = 'room_create'),
    path('room/<int:pk>',RoomView.as_view(),name = 'room'),
    path('room/update/<int:pk>',RoomUpdateView.as_view(),name = 'room_update'),
    path('brons/<int:pk>',BronView.as_view(),name = 'brons'),
    path('add/bron/<int:pk>',BronAddView.as_view(),name = 'add_bron'),
    path('cancel/bron',BronCancelView.as_view(),name = 'cancel_bron')

]
