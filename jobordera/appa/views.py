from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appa.model import userinfo, loginhistory, checklisttemplte, formfilelist
from django.db import connection, connections, models
import logging
import datetime
import os
import json

mylog = logging.getLogger('myproject.custom')
filepath = "D:\\project\\program\\python-web-2019\\imagefiles"


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
    try:
        btime = request.POST.get('btime')
        etime = request.POST.get('etime')
    except:
        pass
    if (status is None) | (request.session['userkind'] != 'adminer'):
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            request.session['htmlname'] = "admin.html"
            return render(request, 'admin.html', {"list": [], "refrash": ""})
        elif request.method == "POST":
            data = None
            if (request.POST.get("checklisttemplate") is not None) | (
                        request.session['htmlname'] == "checklisttemplate.html"):
                request.session['htmlname'] = "checklisttemplate.html"
                retrundata = checklisttemplate(request)
                return render(request, 'checklisttemplate.html', retrundata)
            elif (request.POST.get("usehistory") is not None) | (
                        request.session['htmlname'] == "usehistory.html"):
                request.session['htmlname'] = "usehistory.html"
                retrundata = usehistory(request)
                return render(request, 'usehistory.html', retrundata)
            else:
                request.session['htmlname'] = "admin.html"
                if request.POST.get("check"):
                    data = admincheck(username)
                elif request.POST.get("add"):
                    data = adminadd(username, usercode, usertype)
                    os.mkdir(filepath + "./" + username)
                elif request.POST.get("all"):
                    data = adminall()
                return render(request, 'admin.html', {"list": data, "refrash": username})


def user(request):

    status = request.COOKIES.get("name")
    usrname = request.session['username']
    templteselected = request.POST.get('templteselect')
    try:
        btime = request.POST.get('btime')
        etime = request.POST.get('etime')
    except:
        pass

    formfilekind = ""
    formlist = [""]

    if (status is None) | (request.session['userkind'] != 'user'):
        return HttpResponseRedirect('../')
    else:
        cursor = connection.cursor()
        formnames = cursor.execute("select templtename from appa_checklisttemplte").fetchall()

        if templteselected is None:
            templteselected = formnames[0][0]

        formmessage = cursor.execute(
            "select formlist,templtekind from appa_checklisttemplte where templtename='" + templteselected + "'").fetchall()
        if len(formmessage) >= 1:
            formlist = json.loads(formmessage[0][0])
            formfilekind = formmessage[0][1]

        userdata = {"testloop": formlist, "namelist": formnames, "eachfile": [{"name": "", "size": 0}],
                    "selectnow": "","eachfile":""}
        if request.method == "GET":
            request.session['htmlname'] = "user.html"
            return render(request, 'user.html', userdata)
        elif request.method == "POST":
            formfileid = 1
            userdata2 = {"formnamelist": ["", ""], "formcantans": ["", ""], "selectednow": 0}
            if (request.POST.get("usehistory") is not None) | (
                        request.session['htmlname'] == "usehistory.html"):
                request.session['htmlname'] = "usehistory.html"
                retrundata = usehistory(request)
                return render(request, 'usehistory.html', retrundata)
            elif (request.POST.get("myform") is not None) | (
                        request.session['htmlname'] == "myform.html"):
                request.session['htmlname'] = "myform.html"
                if request.POST.get("myform"):
                    userdata2['formnamelist'] = myform(request, usrname, formfileid)
                    request.session['formnamelist'] = userdata2['formnamelist']
                else:
                    userdata2['selectednow'] = int(request.POST.get("templteselect"))
                    formbase=myform(request, usrname, str(userdata2['selectednow']))
                    userdata2['eachfile']=formbase[0][1]
                    userdata2['formcantans'] = json.loads(formbase[0][0])
                    userdata2['formnamelist'] = request.session['formnamelist']
                return render(request, 'myform.html', userdata2)
            else:
                request.session['htmlname'] = "user.html"
                if request.POST.get("updata"):
                    formcantain = request.POST.get("formcantain")
                    files = request.FILES.getlist('chosefiles')
                    upformdata(files, usrname, formfilekind, templteselected, formcantain)
                    operationmark(usrname, "updata")
                    userdata['result']=files
                    return render(request, 'user.html', userdata)
                elif request.POST.get("templteselect"):
                    userdata['testloop'] = formlist
                    userdata['namelist'] = formnames
                    userdata['result'] = [{"name": "", "size": 0}]
                    userdata['selectnow'] = templteselected
                    return render(request, 'user.html', userdata)


def set_cookietest(HttpResponseRedirect):
    co = HttpResponseRedirect.set_cookie("name", "coa", expires=300)
    return co


def usehistory(request):
    btime = request.POST.get('btime')
    etime = request.POST.get('etime')
    retrundata = {"list": [], "btime": "", "etime": ""}
    if request.POST.get("serch"):
        data = serch(btime, etime)
        retrundata['list'] = data
        retrundata['btime'] = btime
        retrundata['etime'] = etime
    return retrundata


def upformdata(form, usrname, formfilekind, formtempltename, formcantain):
    # 读取基础信息
    cursor = connection.cursor()
    k = cursor.execute("select max(formfileid) from appa_formfilelist where uploader='" + usrname + "'").fetchall()[0][
        0]
    if k is None:
        k = 0
    # 读取文档
    fileaddress = list()
    for eachfile in form:
        timemark = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
        name = usrname + "//" + str(k + 1) + "_" + formtempltename + "_" + str.replace(timemark, ":",
                                                                                       "_") + "_" + eachfile.name
        with open(filepath + "//" + name, 'wb') as f:
            for i in eachfile.chunks():
                f.write(i)
        fileaddress.append(name)

    # 信息写库
    formtime = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
    if k is None:
        k = 0
    formfilelist.objects.create(formfileid=k + 1, formfilename=formtempltename, formfilekind=formfilekind,
                                createtime=formtime, formcantain=formcantain, fileaddress=fileaddress, uploader=usrname)
    return fileaddress


def checklisttemplate(request):
    retrundata = {"httempltename": "", 'resultlist': [["", "", ""]], 'file': "", "othinfo": ["", "", ""],
                  "namelist": [""], "selectnow": ""}
    cursor = connection.cursor()
    request.session['templtenamelist'] = cursor.execute(
        "select templtename from appa_checklisttemplte").fetchall()
    # 返回值
    retrundata['namelist'] = request.session['templtenamelist']
    retrundata['selectnow'] = request.POST.get("templtename")

    if request.POST.get("searchtemplte"):
        templtename = request.POST.get("templteselect")
        tform = checklisttemplte.objects.filter(templtename=templtename).values()[0]
        # 返回值
        retrundata['httempltename'] = tform['templtename']
        retrundata['resultlist'] = json.loads(tform['formlist'])
        retrundata['othinfo'] = [tform['templteid'], tform['templtekind'], tform['createtime']]
        retrundata['namelist'] = request.session['templtenamelist']
        retrundata['selectnow'] = templtename
        retrundata['file'] = tform['fileaddress']
    elif request.POST.get("addtemplte"):
        retrundata['selectnow'] = request.POST.get("templtename")
        retrundata['namelist'] = addtemplate(templtename=request.POST.get("templtename"),
                                             templtekind=request.POST.get("templtekind"),
                                             formlist=request.POST.get("formlist"))
    elif request.POST.get("deletetemplte"):
        deletetemplate(request.POST.get("templteselect"))
        cursor = connection.cursor()
        request.session['templtenamelist'] = cursor.execute(
            "select templtename from appa_checklisttemplte").fetchall()
        # 返回值
        retrundata['namelist'] = request.session['templtenamelist']
    return retrundata


def addtemplate(templtename, templtekind, formlist):

    cursor = connection.cursor()
    k = cursor.execute("select max(templteid) from appa_checklisttemplte").fetchall()[0][0]
    if k is None:
        k = 0
    checklisttemplte.objects.create(templteid=k + 1, templtename=templtename, templtekind=templtekind,
                                    formlist=formlist)
    templtenamelist = cursor.execute("select templtename from appa_checklisttemplte").fetchall()
    return templtenamelist


def deletetemplate(templtename):
    cursor = connection.cursor()
    k = cursor.execute("delete  from appa_checklisttemplte where templtename='" + templtename + "'").fetchall()
    return None


def strtolist(strs):
    la = list()
    al = strs.split(";")
    index = 0
    for i in al:
        la.append(list(i.split(',')) + [str(index)])
        index = index + 1
    return la[:-1]


def strtolistfrombase(str):
    la = list()


def myform(request, name, formfileid):
    cursor = connection.cursor()
    if request.POST.get("myform"):
        formnamelist = cursor.execute(
            "select formfileid,formfilename from appa_formfilelist where uploader='" + name + "'").fetchall()
        return formnamelist
    else:
        formmessage = cursor.execute(
            "select formcantain,fileaddress from appa_formfilelist where formfileid='" + formfileid + "' and uploader='" + name + "'").fetchall()
        return formmessage


def gettemplteitem(request):
    temp=request.POST.get("len")

    return None
