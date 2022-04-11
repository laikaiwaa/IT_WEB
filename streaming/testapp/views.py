# coding=utf-8
import time

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
    r=0
    while (True):
        r=r+0.01
        time.sleep(0)
        im = ImageGrab.grab()
        #frame = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        frame=cv2.imread("/root/liekiewaa/web/imagefiles/static/ocean.jpg")
        sp=frame.shape	

        if (r<=0.001) | (r>1):
		r=0.01
        frame=frame[:int(sp[0]*r),:int(sp[1]*r),:]

        _, g = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n\r\n' + g.tobytes() + b'\r\n\r\n')


def sendvideo(request):
    return StreamingHttpResponse(makepicture(), content_type="multipart/x-mixed-replace;boundary=frame")


def watchcontrol(request):
    if request.method == "GET":
        return render(request, 'watch.html')
    #if request.method =="POST":
    #    if request.POST.get("close"):
   #         return render(request, 'watch.html')
