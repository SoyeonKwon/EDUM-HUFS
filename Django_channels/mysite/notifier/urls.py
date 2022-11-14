from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^$', views.change_stat),
    path("home/change_stat", views.database_handler),
    path("home/send_weight", views.send_weight),
    path('monitor/home/alert.html',views.AlertView.as_view(), name = 'alert'),
    #path('audios/note.mp3',views.AlertView),
    path('edum/',auth_views.LoginView.as_view(), name='login'),
   # path('monitor/sms',views.run, name='run'),
    url(r'streamtest/', views.livefe, name='livefe'),
    url(r'streamtest1/', views.livefe1, name='livefe1'),
    url(r'streamtest2/', views.livefe2, name='livefe2'),
    url(r'loginteste/', views.profile, name='profile'),
    url(r'resident/', views.resident, name='resident'),
    url(r'^residentcam0/$', views.residentcam0, name='residentcam0'),
    url(r'^residentcam1/$', views.residentcam1, name='residentcam1'),
    url(r'img/backg', views.imgbackg, name='imgbackg'),
    url(r'img/edumimg', views.imgedumimg, name='imgedumimg'),
]