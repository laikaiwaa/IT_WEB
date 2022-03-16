from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appa.model import userinfo, loginhistory
from django.db import connection, connections, models
import logging
import datetime
import os

mylog = logging.getLogger('myproject.custom')
filepath = "c:\\liekiewaa\\web\\imagefiles"


def logincheck(ausername, busercode):
    result = userinfo.objects.filter(username=ausername, password=busercode).values()
    if result:
        return result[0]['type']
    else:
        return []


def operationmark(ausername, aactionkind):
    uid = userinfo.objects.filter(username=ausername).values()[0]['userid']
    loginhistory.objects.create(userid=uid, username=ausername, actionkind=aactionkind)


def adminall():
    result = userinfo.objects.all().values()
    return result


def admincheck(ausername):
    result = userinfo.objects.filter(username=ausername).values()
    return result


def adminadd(ausername, busercode, cusertype):
    cursor = connection.cursor()
    k = cursor.execute("select count(*) from appa_userinfo").fetchall()[0][0]
    userinfo.objects.create(userid=k + 1, username=ausername, password=busercode, type=cusertype)
    select = userinfo.objects.all().values()
    return select


def serch(b, e):
    cursor = connection.cursor()
    sql = "select * from appa_loginhistory where  time >=datetime('" + b + " 00:00:00.000000') " \
                                                                           "and time <=datetime('" + e + " 23:59:59.000000') " \
        # sql="select * from appa_loginhistory where WHERE time >=time('"+b+ " 0:0:0') " \
    #                "and time <=time('"+e+ " 23:59:59') "  \
    l = cursor.execute(sql)
    result = l.fetchall()
    if result:
        return result


def login(request):
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        if request.POST.get("login"):
            logic = logincheck(username, usercode)
            operationmark(username, "login")
            if logic == 'admin':
                a = HttpResponseRedirect('admin')
                set_cookietest(a)
                request.session['userkind'] = 'adminer'
                request.session['username'] = username
                return a
            if logic == 'user':
                a = HttpResponseRedirect('user')
                set_cookietest(a)
                request.session['userkind'] = 'user'
                request.session['username'] = username
                return a
            else:
                return render(request, 'login.html')


def admin(request):
    status = request.COOKIES.get("name")
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    usertype = request.POST.get('usertype')
    if (status is None) | (request.session['userkind'] != 'adminer'):
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            return render(request, 'admin.html', {"list": [], "refrash": ""})
        elif request.method == "POST":
            data = None
            if request.POST.get("check"):
                data = admincheck(username)
                # return render(request, 'admin.html', {"list": data, "refrash": username})
            elif request.POST.get("add"):
                data = adminadd(username, usercode, usertype)
                os.mkdir(filepath + "./" + username)
            elif request.POST.get("all"):
                data = adminall()
            elif request.POST.get("usehistory"):
                #return render(request, 'usehistory.html')
                return HttpResponseRedirect('../usehistory')
            elif request.POST.get("checklisttemplate"):
                #return render(request, 'checklisttemplate.html', {"list": data, "refrash": username})
                return HttpResponseRedirect('/checklisttemplate')
            return render(request, 'admin.html', {"list": data, "refrash": username})


def usehistory(request):
    status = request.COOKIES.get("name")
    btime = request.POST.get('btime')
    etime = request.POST.get('etime')
    if status is None:
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            return render(request, 'usehistory.html', {"list": [], "btime": "", "etime": ""})
        elif request.method == "POST":
            if request.POST.get("serch"):
                data = serch(btime, etime)
                return render(request, 'usehistory.html', {"list": data, "btime": btime, "etime": etime})


def user(request):
    status = request.COOKIES.get("name")
    usrname = request.session['username']
    testloop = [i for i in range(3)]

    if (status is None) | (request.session['userkind'] != 'user'):
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":

            return render(request, 'user.html',{"testloop":testloop})
        elif request.method == "POST":
            if request.POST.get("usehistory"):
                return HttpResponseRedirect('../usehistory')
            elif request.POST.get("updata"):
                checkboxlist = [[testloop[i], request.POST.get("checkbox" + str(i))] for i in range(3)]
                print(checkboxlist)
                files = request.FILES.getlist('chosefiles')
                upformdata(files, usrname)
                return render(request, 'user.html', {"result": files})


def set_cookietest(HttpResponseRedirect):
    co = HttpResponseRedirect.set_cookie("name", "coa", expires=300)
    return co


def upformdata(form, usrname):
    for eachfile in form:
        timemark = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
        with open(filepath + "\\" + usrname + "\\" + str.replace(timemark, " :", "_") + "_" + eachfile.name, 'wb') as f:
            for i in eachfile.chunks():
                f.write(i)
    return None

def checklisttemplate(request):
    status = request.COOKIES.get("name")
    cursor = connection.cursor()
    templtenamelist = cursor.execute("select templtename from appa_checklisttemplte").fetchall()
    if (status is None) :
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            return render(request, 'checklisttemplate.html', {"list": templtenamelist})
        elif request.method == "POST":
            data = None
            if request.POST.get("addtemplte"):
                data = admincheck()
                return HttpResponseRedirect('/checklisttemplate')
            return render(request, 'admin.html', {"list": data})
    return None
