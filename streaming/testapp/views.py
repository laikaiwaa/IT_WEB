# coding=utf-8
import time
import base64

from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
# import testapp.model as md
# from testapp.model import userinfo, loginhistory, checklisttemplte, formfilelist
from django.db import connection, connections, models
import logging
import datetime
import os
import json
from django.contrib.auth.hashers import make_password, check_password
import random
import hashlib

mylog = logging.getLogger('myproject.custom')
salt = b'liekiewaa'

from PIL import ImageGrab
import cv2
import numpy as np


def makepicture():
    r = 0
    while (True):
        r = r + 0.01
        time.sleep(0)
        # im = ImageGrab.grab()
        # frame = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        path="E:/manualmaintenance/imagefiles/"
        try:
            dirs=os.listdir(path)
            dirs.sort()
            for i in dirs:
                if i.__contains__(".jpg"):
                    frame = cv2.imread(path+i)
                    _, g = cv2.imencode('.jpg', frame)
                    yield (b'--frame\r\n'
                           b'Content-Type:image/jpeg\r\n\r\n' + g.tobytes() + b'\r\n\r\n')
                    os.remove(path+i)
        except:
            time.sleep(5)
        # sp = frame.shape
        #
        # if (r <= 0.001) | (r > 1):
        #     r = 0.01
        # frame = frame[:int(sp[0] * r), :int(sp[1] * r), :]

        # _, g = cv2.imencode('.jpg', frame)




def sendvideo(request):
    return StreamingHttpResponse(makepicture(), content_type="multipart/x-mixed-replace;boundary=frame")

# 寫成視頻文件
def watchcontrol(request):
    if request.method == "GET":
        return render(request, 'watch.html')
    if request.method == "POST":
        if request.POST.get("sendmark"):
            form = request.POST.get("stream").split(",")[1]
            image2 = base64.b64decode(form)
            # 写入档案
            tempfilepath = "E:/manualmaintenance/imagefiles/img_"+str(datetime.datetime.now().time()).replace(":","_")+".jpg"
            tempfilepathv = "E:/manualmaintenance/imagefiles/img.avi"
            # try:
            #     w=cv2.VideoCapture(tempfilepathv)
            # except:
            #     w = cv2.VideoWriter(tempfilepathv, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60,
            #                              (500, 500))
            try:
                with open(tempfilepath, 'wb') as f:
                    f.write(image2)
                    f.close
                # img=cv2.imread(tempfilepath)
                # w.write(img)
            except Exception as dd:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", dd)
            return render(request, 'watch.html')
# def watchcontrol(request):
#     if request.method == "GET":
#         return render(request, 'watch.html')
#     if request.method == "POST":
#         if request.POST.get("sendmark"):
#             form = request.POST.get("stream").split(",")[1]
#             image2 = base64.b64decode(form)
#             # 写入档案
#             tempfilepath = "E:/manualmaintenance/imagefiles/img.jpg"
#             try:
#                 with open(tempfilepath, 'wb') as f:
#                     f.write(image2)
#                     f.close
#             except Exception as dd:
#                 print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", dd)
#             return render(request, 'watch.html')
