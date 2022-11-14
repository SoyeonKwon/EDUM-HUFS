from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Camera, Profile
from django.views.decorators.csrf import csrf_exempt
import urllib.parse as urlparse
import json
from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import cv2
import numpy as np
from django.http import StreamingHttpResponse
import threading
from django.views.decorators.gzip import gzip_page
import gzip
from django.http import JsonResponse
from time import sleep

class HomeView(TemplateView):
    template_name = "home/home.html"


def profile(request):
    if request.method == "GET":
        name = request.user.get_username()
    if name == 'Jun':
        print("Yes!")
    return render(request, 'home/resident.html')
    profile = Profile.objects.all()
    for pro in profile:
        if str(pro.user) == name:
            pro.loginchk = True
            pro.save()
        else:
            pro.loginchk = False
            pro.save()

    return HttpResponse("%s is login", name)

def resident(request):
    return render(request, 'home/resident.html')

def residentcam0(request):
    print("ye")
    return render(request, 'home/residentcam0.html')

def residentcam1(request):
    print("no")
    return render(request, 'home/residentcam1.html')








# def homeview(request):
#     # profile = Profile.objects.all()
#         profile.loginchk = True
#         profile.save()
#     return render(request, 'home/home.html')


# def alert(request):
#     cams = Camera.objects.all()
#     context = {'cams': cams}
#     return render(request, 'home/alert.html', context)
class AlertView(TemplateView):
    def get(self,request,*args, **kwargs):
        cams = Camera.objects.all()
        context = {'cams': cams}
        return render(request, 'home/alert.html', context)

def send_weight(request):
    cams = Camera.objects.all()
    weight = dict([(i, None) for i in range(len(cams))])
    for cam in cams:
        weight[cam.cam_id] = cam.weight
    return JsonResponse(weight)

@csrf_exempt
def database_handler(request):
    cams = Camera.objects.all()
    if request.method == "POST":
        decoded_data = request.read().decode('utf-8')
        # print(decoded_data)
        dict_data = json.loads(decoded_data)
        print("#####Dict######:", dict_data)
        cam_id = dict_data['cam_id']
        # cam_status = dict_data['cam_status']
        # cam_location = dict_data['cam_location']
        cam_fallen = dict_data['fallen']
        cam_trash = dict_data['trash']
        cam_instrusion = dict_data['intrusion']
        cam_fence = dict_data['fence']

        print("----values=====:", cam_id, cam_trash, cam_instrusion,cam_fallen,cam_fence)
        print("#################value types:",type(cam_trash))

        for cam in cams:
            if (cam.cam_id == cam_id):
                print("Camera table has been changed!#!@#@!#")
                # cam.cam_status = cam_status
                # cam.cam_location = cam_location
                cam.fallen = cam_fallen
                cam.trash = cam_trash
                cam.instrusion = cam_instrusion
                cam.fence = cam_fence
                evnet_hadler(cam)
            if cam.cam_status == 'warning':
                phone = ''
                profile = Profile.objects.all()
                for pro in profile:
                    if (pro.loginchk):
                        phone = pro.phone_number
                print("Let's check PHONE : ", pro.loginchk, pro.phone_number, phone)
                send = Sendsms(phone, cam.cam_location, cam.fallen, cam.trash,cam.instrusion,cam.fence)
                send.sendSms()
            cam.save()
    return HttpResponse("OK")

def evnet_hadler(cam):
    if (cam.fallen or cam.trash or cam.fence or cam.instrusion):
        cam.weight = 1  # defalut priority of camera
        if cam.fallen:
            cam.weight += 2
        if cam.trash:
            cam.weight += 1
        if cam.instrusion:
            cam.weight += 3
        if cam.fence:
            cam.weight += 3
        cam.cam_status = 'warning'
    # elif not (cam.fallen or cam.trash or cam.fence or cam.instrusion):
    else:
        cam.cam_status = 'safe'
        cam.weight = 1  # default weight per camera





class StreamingVideo(object):
    def __init__(self):
        self.k = True
        self.index = 0
        self.slep = 0

    def get_frame(self, camid):
        sleep(0.5)
        try :
            name = '/img_{}.png'.format(cam.index)
            image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/' + str(camid) + name)
            ret, jpeg = cv2.imencode('.jpg', image)
        except :
            if cam.index == 0:
                cam.index = 2
            else: cam.index -= 1
            name = '/img_{}.png'.format(cam.index)
            image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/' + str(camid) + name)
            ret, jpeg = cv2.imencode('.jpg', image)
        else:
            cam.index += 1
        if cam.index % 3 == 0:
            cam.index = 0
        return jpeg.tobytes()

cam = StreamingVideo() #서버 실행시 최초 1회만 실행

def gen(camera):
    while True:
        frame = cam.get_frame(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)

def gen1(camera):
    while True:
        frame = cam.get_frame(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#@gzip.gzip_page
def livefe1(request):
    try:
        return StreamingHttpResponse(gen1(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)

def gen2(camera):
    while True:
        frame = cam.get_frame(2)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#@gzip.gzip_page
def livefe2(request):
    try:
        return StreamingHttpResponse(gen1(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)
        
def img():
    image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/backg2.jpg')
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def imgbackg(request):
    try:
        return StreamingHttpResponse(img(), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)

def img2():
    image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/edum.gif')
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def imgedumimg(request):
    try:
        return StreamingHttpResponse(img2(), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)


def img():
    image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/backg2.jpg')
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def imgbackg(request):
    try:
        return StreamingHttpResponse(img(), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)

def img2():
    image = cv2.imread('C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/edum.gif')
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def imgedumimg(request):
    try:
        return StreamingHttpResponse(img2(), content_type="multipart/x-mixed-replace;boundary=frame")
    except ConnectionAbortedError as e:
        print(e)

# def update_profile(request, user_id):
#    user = User.objects.get(pk=user_id)
#    user.save()
import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException



class Sendsms:
    def __init__(self, phone_number, place, fallen,trash,intrusion,fence):
        self.phone_number = phone_number
        self.place = place
        self.text = ''
        if fallen:
            self.text += '쓰러진 사람감지 '
        if trash:
            self.text += "쓰레기 감지 "
        if intrusion:
            self.text += "접근 제한 구역 침입 감지 "
        if fence:
            self.text += "월담 행위 감지 "

    def sendSms(self):
        # set api key, api secret
        api_key = "NCS6DX5TVMC0XKUF"
        api_secret = "QAGSWWBHCMTBZFEOQK6G0KMZE4DMJRBH"

        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = self.phone_number # Recipients Number '01000000000,01000000001'
        params['from'] = '01035419130'  # Sender number
        params['text'] = self.place + ' 카메라에 ' + self.text + '가 발생하였습니다.' # Message

        cool = Message(api_key, api_secret)

        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        # sys.exit()

