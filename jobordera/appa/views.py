# coding=utf-8
from django.http import HttpResponse, FileResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import appa.model as md
from appa.model import userinfo, loginhistory, checklisttemplte, formfilelist
from django.db import connection, connections, models
import logging
import datetime
import os
import json

mylog = logging.getLogger('myproject.custom')


def settingg():
    filepath = "/root/liekiewaa/web/imagefiles"
    return filepath


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
            if request.GET.get('back'):
                return HttpResponseRedirect("../admin/")
            else:
                request.session['htmlname'] = "admin.html"
                return render(request, 'admin.html', {"list": [], "refrash": ""})
        elif request.method == "POST":
            data = ""
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
            # 处理退出
            elif request.POST.get("quit"):
                return HttpResponseRedirect("../")
            else:
                request.session['htmlname'] = "admin.html"
                if request.POST.get("check"):
                    data = admincheck(username)
                elif request.POST.get("add"):
                    data = adminadd(username, usercode, usertype)
                    filepath = settingg()
                    os.mkdir(filepath + "/" + username)
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
            formlist = json.loads(formmessage[0][0].encode(encoding="utf8"))
            formfilekind = formmessage[0][1].encode(encoding="utf8")

        userdata = {"testloop": formlist, "namelist": formnames, "result": [{"name": "", "size": 0}],
                    "selectnow": "", "username": request.session['username'], "formnamelist": ["", ""]}

        if request.method == "GET":
            if request.GET.get('checkform'):
                formbase = myform(request, usrname, request.GET.get('checkform'))
                userdata = {
                    'formfilename': formbase['formfilename'],
                    'fileaddres': json.loads(formbase['fileaddress']),
                    'uploadpermi': 'edit',
                    'username': usrname
                }
                if formbase['filestatus'] in ('已上传'):
                    userdata['readmodel'] = 'read'
                else:
                    userdata['readmodel'] = 'edit'
                if formbase['formfilekind'] == 'FL':
                    userdata['formcantain'] = htmlitemname("FL", json.loads(formbase['formcantain']))
                    request.session['htmlname'] = "job_fileslist.html"
                    return render(request, 'job_fileslist.html', userdata)
                else:
                    userdata['formcantain'] = htmlitemname("CL", json.loads(formbase['formcantain']))
                    request.session['htmlname'] = "job_systemchecklist.html"
                    return render(request, 'job_systemchecklist.html', userdata)
            elif request.GET.get('back'):
                return HttpResponseRedirect("../user/")
            else:
                userdata['formnamelist'] = myform(request, usrname)
                request.session['htmlname'] = "user.html"
                return render(request, 'user.html', userdata)
        elif request.method == "POST":
            formfileid = 1
            userdata2 = {"formnamelist": ["", ""], "formcantans": [{"itemm": "", "statuss": ""}], "selectednow": 0,
                         "fileaddres": "", "username": request.session['username']}
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
                    return render(request, 'myform.html', userdata2)
                else:
                    if request.POST.get("filename"):
                        h = downfile(request.POST.get("filename"))
                        return h
                    # 处理查看
                    else:
                        userdata2['selectednow'] = int(request.POST.get("templteselect"))
                        formbase = myform(request, usrname, str(userdata2['selectednow'])) 
                        userdata2['fileaddres'] = json.loads(formbase[0][1].replace("'", "\""))
                        userdata2['formcantans'] = json.loads(formbase[0][0])
                        userdata2['formnamelist'] = request.session['formnamelist']
                        return render(request, 'myform.html', userdata2)
            # 处理新增
            elif request.POST.get('form_fileslist') or request.POST.get('form_syschecklist'):
                operationmark(usrname, "添加表单")
                h2 = addnewform(request)
                return h2
            # 处理退出
            elif request.POST.get("quit"):
                return HttpResponseRedirect("../")
            # 处理下载
            elif request.POST.get("filename"):
                h = downfile(request.POST.get("filename"))
                return h
            # 处理上传
            else:
                if request.POST.get("update"):
                    files = request.FILES.getlist('chosefiles')
                    filepath = settingg()
                    if request.POST.get("updatereflush"): 
                        upformdata(filepath, files, usrname, request.POST, "update")
                        operationmark(usrname, "updata")
                        userdata = {"formfilename": "", "username": usrname,
                                    "formcantain": htmlitemname(request.POST.get('formfilename')[:2], valueditem=None),
                                    "readmodel": 'edit', 'uploadpermi': 'edit', "fileaddres": []}
                        return render(request, request.session['htmlname'], userdata)
                    else:
                        h2 = addnewform(request)
                        return h2

                elif request.POST.get("tempsave"):
                    files = request.FILES.getlist('chosefiles')
                    filepath = settingg()
                    if request.POST.get("updatereflush"):
                        upformdata(filepath, files, usrname, request.POST, "tempsave")
                        operationmark(usrname, "updata")
                        userdata = {"formfilename": "", "username": usrname,
                                    "formcantain": htmlitemname(request.POST.get('formfilename')[:2], valueditem=None),
                                    "readmodel": 'edit', 'uploadpermi': 'edit', "fileaddres": []}
                        return render(request, request.session['htmlname'], userdata)
                    else:
                        h2 = addnewform(request)
                        return h2


def htmlitemname(kind, valueditem=None):
    if kind == 'FL':
        formcantainitem = {
            'formfilename': '', 'projectname': '', 'producttype': '', 'data': '', 'projectmember': '',
            'item11mark': '', 'item11date': '', 'person11': '', 'remarks11': '',
            'item12mark': '', 'item12date': '', 'person12': '', 'remarks12': '',
            'item13mark': '', 'item13date': '', 'person13': '', 'remarks13': '',
            'item14mark': '', 'item14date': '', 'person14': '', 'remarks14': '',
            'item15mark': '', 'item15date': '', 'person15': '', 'remarks15': '',
            'item16mark': '', 'item16date': '', 'person16': '', 'remarks16': '',
            'item17mark1': '', 'item17mark2': '', 'item17date': '', 'person17': '', 'remarks17': '',
            'item21mark': '', 'item21date': '', 'person21': '', 'remarks21': '',
            'item22mark': '', 'item22date': '', 'person22': '', 'remarks22': '',
            'item23mark': '', 'item23date': '', 'person23': '', 'remarks23': '',
            'item24mark': '', 'item24date': '', 'person24': '', 'remarks24': '',
            'item25mark': '', 'item25date': '', 'person25': '', 'remarks25': '',
            'item26mark': '', 'item26date': '', 'person26': '', 'remarks26': ''
        }
    if kind == 'CL':
        formcantainitem = {
            'formfilename': '', 'projectname': '', 'producttype': '', 'projectmember': '',
            'item01mark': '', 'item01remarks': '', 'item02mark': '', 'item02remarks': '',
            'item03mark': '', 'item03remarks': '', 'item04mark': '', 'item04remarks': '',
            'item05mark': '', 'item05remarks': '', 'item06mark': '', 'item06remarks': '',
            'item07mark': '', 'item07remarks': '', 'item08mark': '', 'item08remarks': '',
            'item09mark': '', 'item09remarks': '', 'item10mark': '', 'item10remarks': '',
            'item11mark': '', 'item11remarks': '', 'item12mark': '', 'item12remarks': '',
            'item13mark': '', 'item13remarks': '', 'item14mark': '', 'item14remarks': '',
            'item15mark': '', 'item15remarks': '', 'item16mark': '', 'item16remarks': '',
            'item17mark': '', 'item17remarks': '', 'item18mark': '', 'item18remarks': '',
            'item19mark': '', 'item19remarks': '', 'item20mark': '', 'item20remarks': '',
            'item21mark': '', 'item21remarks': '', 'item22mark': '', 'item22remarks': '',
            'item23mark': '', 'item23remarks': '', 'item24mark': '', 'item24remarks': '',
            'item25mark': '', 'item25remarks': '', 'item26mark': '', 'item26remarks': '',
            'item27mark': '', 'item27remarks': '', 'item28mark': '', 'item28remarks': '',
            'item29mark': '', 'item29remarks': '', 'item30mark': '', 'item30remarks': '',
            'item31mark': '', 'item31remarks': '', 'item32mark': '', 'item32remarks': '',
            'item33mark': '', 'item33remarks': '', 'item34mark': '', 'item34remarks': '',
            'item35mark': '', 'item35remarks': '', 'item36mark': '', 'item36remarks': '',
            'item37mark': '', 'item37remarks': '', 'item38mark': '', 'item38remarks': '',
            'item39mark': '', 'item39remarks': '', 'item40mark': '', 'item40remarks': '',
            'item41mark': '', 'item41remarks': '', 'item42mark': '', 'item42remarks': '',
            'item43mark': '', 'item43remarks': '', 'item44mark': '', 'item44remarks': '',
            'item45mark': '', 'item45remarks': '', 'item46mark': '', 'item46remarks': '',
            'item47mark': '', 'item47remarks': '', 'item48mark': '', 'item48remarks': '',
            'item49mark': '', 'item49remarks': '', 'item50mark': '', 'item50remarks': '',
            'item51mark': '', 'item51remarks': '', 'item52mark': '', 'item52remarks': '',
            'item53mark': '', 'item53remarks': '', 'item54mark': '', 'item54remarks': '',
            'item55mark': '', 'item55remarks': '', 'item56mark': '', 'item56remarks': '',
            'item57mark': '', 'item57remarks': ''
        }
    if valueditem is not None:
        for i in formcantainitem:
            try:
                formcantainitem[i] = valueditem[i]
            except:
                pass
    return formcantainitem


def addnewform(request):
    userdata = {}

    if request.POST.get('form_fileslist'):
        request.session['htmlname'] = "job_fileslist.html"
        uploader = request.session['username']
        id = 0
        try:
            id = md.formfilelist.objects.filter(uploader=uploader, formfilekind='FL').aggregate(
                models.Max('formfileid'))[
                     'formfileid__max'] + 1
        except:
            pass
        timemark = str.replace(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d"), "_", "")
        formfilename = "FL" + str(id) + "_" + timemark
        return render(request, 'job_fileslist.html', {"formfilename": formfilename, "username": uploader,
                                                      "formcantain": htmlitemname("FL"), "readmodel": 'edit',
                                                      'uploadpermi': 'edit', "fileaddres": []})
    elif request.POST.get('form_syschecklist'):
        request.session['htmlname'] = "job_systemchecklist.html"
        uploader = request.session['username']
        id = 0
        try:
            id = md.formfilelist.objects.filter(uploader=uploader, formfilekind='CL').aggregate(
                models.Max('formfileid'))[
                     'formfileid__max'] + 1
        except:
            pass
        timemark = str.replace(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d"), "_", "")
        formfilename = "CL" + str(id) + "_" + timemark
        return render(request, 'job_systemchecklist.html', {"formfilename": formfilename, "username": uploader,
                                                            "formcantain": htmlitemname("CL"), "readmodel": 'edit',
                                                            'uploadpermi': 'edit', "fileaddres": []})
    else:
        uploader = request.session['username']
        id = 0
        try:
            id = md.formfilelist.objects.filter(uploader=uploader,
                                                formfilekind=request.POST.get('formfilename')[:2]).aggregate(
                models.Max('formfileid'))[
                     'formfileid__max'] + 1
        except:
            pass
        timemark = str.replace(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d"), "_", "")
        formfilename = request.POST.get('formfilename')[:2] + str(id) + "_" + timemark
        return render(request, request.session['htmlname'], {"formfilename": formfilename, "username": uploader,
                                                             "formcantain": htmlitemname(
                                                                 request.POST.get('formfilename')[:2]),
                                                             "readmodel": 'edit',
                                                             'uploadpermi': 'edit', "fileaddres": []})


def set_cookietest(HttpResponseRedirect):
    co = HttpResponseRedirect.set_cookie("name", "coa", expires=1200)
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


def upformdata(filepath, form, usrname, formcantain, upstatus):
    
    formcantainstr = json.dumps(formcantain)
    # 读取基础信息
    k = int(formcantain['formfilename'][2:formcantain['formfilename'].find("_")])
    # 读取文档
    fileaddress = list()
    # 标记是否有记录
    ifesit = len(formfilelist.objects.filter(formfileid=k, uploader=usrname,formfilekind=formcantain['formfilename'][:2]).values())

    # 查看文件是否存在
    filelist = os.listdir(filepath + "/" + usrname + "/") 
    for i in filelist:
        if i[:i.find('_')] == formcantain['formfilename'][:formcantain['formfilename'].find("_")]:
            fileaddress.append(usrname + "/" + i) 
    # 写入档案
    for eachfile in form:
        name = usrname + "/" + formcantain['formfilename'] + "_" + eachfile.name.replace(" ", "_")
        tempfilepath = filepath + "/" + name
        try:
            with open(tempfilepath, 'wb') as f:
                for i in eachfile.chunks():
                    f.write(i)
                f.close
            fileaddress.append(name)
        except Exception as dd:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", dd, name.encode(encoding="utf-8"))

    # 信息写库 
    formtime = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
    try:
        if upstatus == "update":
            filestatus = "已上传"

        else:
            filestatus = "暂存"
        if ifesit > 0:
            formfilelist.objects.filter(formfileid=k, uploader=usrname).delete()
            formfilelist.objects.create(formfileid=k, formfilename=formcantain['formfilename'],
                                        formfilekind=formcantain['formfilename'][:2],
                                        createtime=formtime, formcantain=formcantainstr,
                                        fileaddress=json.dumps(fileaddress),
                                        uploader=usrname, filestatus=filestatus)
        else:
            
            formfilelist.objects.create(formfileid=k, formfilename=formcantain['formfilename'],
                                        formfilekind=formcantain['formfilename'][:2],
                                        createtime=formtime, formcantain=formcantainstr,
                                        fileaddress=json.dumps(fileaddress),
                                        uploader=usrname, filestatus=filestatus)
    except Exception as aa:
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", aa)

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
        if request.POST.get("addtempltereflush"):
            retrundata['selectnow'] = request.POST.get("templtename")
            retrundata['namelist'] = addtemplate(templtename=request.POST.get("templtename"),
                                                 templtekind=request.POST.get("templtekind"),
                                                 formlist=request.POST.get("formlist"))
        else:
            request.session['templtenamelist'] = cursor.execute(
                "select templtename from appa_checklisttemplte").fetchall()
            retrundata['namelist'] = request.session['templtenamelist']
            retrundata['selectnow'] = request.POST.get("templtename")
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


def myform(request, name, formfilename=None):
    cursor = connection.cursor()
    if formfilename is None:
        formnamelist = cursor.execute(
            "select formfileid,formfilename,filestatus from appa_formfilelist where uploader='" + name + "'").fetchall()
        return formnamelist
    else:
        formmessage = md.formfilelist.objects.filter(uploader=name, formfilename=formfilename).values()[0]
        return formmessage


def gettemplteitem(request):
    temp = request.POST.get("len")

    return None


def sendfiles(request, fileaddress):
    filepath = settingg()
    with open(filepath + "/" + fileaddress, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename={0}'.format("file_name")
    return response


def downfile(name):
    path = settingg() + "//" + name
    re = FileResponse(open(path, 'rb'))
    re['Content-Type'] = 'application/octet-stream'
    re['Content_Disposition'] = 'attachment;filename=' + name + ''
    return re
