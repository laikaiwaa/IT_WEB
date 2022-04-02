# coding=utf-8
from django.http import HttpResponse, FileResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import appa.model as md
from appa.model import userinfo, loginhistory, checklisttemplte, formfilelist
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


def settingg():
    filepath = "/root/liekiewaa/web/imagefiles"
    return filepath


def codesha(code):
    h = hashlib.sha1(salt)
    h.update(code.encode('utf-8'))
    return h.hexdigest()


# 登录验证
def logincheck(ausername, busercode):
    result = userinfo.objects.filter(username=ausername, password=codesha(busercode)).values()
    if result:
        return result[0]['type']
    else:
        return []


# 操作记录
def operationmark(ausername, aactionkind):
    uid = userinfo.objects.filter(username=ausername).values()[0]['userid']
    loginhistory.objects.create(userid=uid, username=ausername, actionkind=aactionkind)


# 用户管理
def adminuser(adminuserkind, username, busercode, cusertype):
    # 查全
    if adminuserkind == "all":
        return userinfo.objects.all().values()
    # 查
    if adminuserkind == "check":
        return userinfo.objects.filter(username=username).values()
    # 增
    if adminuserkind == "add":
        if username.strip() != "":
            filepath = settingg()
            os.mkdir(filepath + "/" + username)
            k = userinfo.objects.aggregate(models.Max('userid'))['userid__max']
            userinfo.objects.create(userid=k + 1, username=username, password=codesha(busercode), type=cusertype)
            return userinfo.objects.all().values()
        else:
            return ["用户名空白"]
    # 删
    if adminuserkind == "delete":
        userinfo.objects.filter(username=username).delete()
        return userinfo.objects.all().values()


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


def check_decorate(fun):
    def wrapper(request, *args, **kwargs):
        if check_password(request.session['code'], request.session['key']):
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("../")

    return wrapper


def login(request):
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        if request.POST.get("login"):
            logic = logincheck(username, usercode)
            operationmark(username, "login")

            request.session['code'] = make_password(usercode, str(random.randint(0, 9)), "pbkdf2_sha1")
            request.session['key'] = make_password(request.session['code'], str(random.randint(0, 9)), "pbkdf2_sha1")
            if username=='x':
                a = HttpResponseRedirect('xuser')
                set_cookietest(a)
                request.session['userkind'] = 'user'
                request.session['username'] = username
                return a
            else:
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


@check_decorate
def admin(request):
    status = request.COOKIES.get("name")
    searchusername = request.POST.get('username')
    usercode = request.POST.get('usercode')
    usertype = request.POST.get('usertype')

    if (status is None) | (request.session['userkind'] != 'adminer'):
        return HttpResponseRedirect('../')
    else:
        sendata = dict(list=[], searchusername="", loginusername=request.session['username'])
        if request.method == "GET":
            if request.GET.get('back'):
                return HttpResponseRedirect("../admin/")
            else:
                request.session['htmlname'] = "admin.html"
                return render(request, 'admin.html', sendata)
        elif request.method == "POST":
            # 处理报表模板
            if (request.POST.get("checklisttemplate") is not None) | (
                    request.session['htmlname'] == "checklisttemplate.html"):
                request.session['htmlname'] = "checklisttemplate.html"
                retrundata = checklisttemplate(request)
                return render(request, 'checklisttemplate.html', retrundata)
            # 处理用户历史
            elif (request.POST.get("usehistory") is not None) | (
                    request.session['htmlname'] == "usehistory.html"):
                request.session['htmlname'] = "usehistory.html"
                retrundata = usehistory(request)
                return render(request, 'usehistory.html', retrundata)
            # 处理退出
            elif request.POST.get("quit"):
                return HttpResponseRedirect("../")
            # 用户处理
            else:
                request.session['htmlname'] = "admin.html"
                if request.POST.get("adminuserkind"):
                    data = adminuser(request.POST.get("adminuserkind"), searchusername, usercode, usertype)
                sendata['list'] = list(data)
                sendata['searchusername'] = searchusername

                return JsonResponse(sendata)


@check_decorate
def user(request):
    status = request.COOKIES.get("name")
    usrname = request.session['username']

    if (status is None) | (request.session['userkind'] != 'user'):
        return HttpResponseRedirect('../')
    else:

        # formnames = list(checklisttemplte.objects.values('templtename'))
        # if templteselected is None:
        #    templteselected = formnames[0]['templtename']
        # formmessage = list(checklisttemplte.objects.filter(templtename= templteselected).values('formlist','templtekind'))

        # if len(formmessage) >= 1:
        #    formlist = json.loads(formmessage[0]['formlist'].encode(encoding="utf8"))
        #    formfilekind = formmessage[0]['templtekind'].encode(encoding="utf8")

        userdata = dict(testloop=[""], result=[{"name": "", "size": 0}], selectnow="",
                        username=request.session['username'], formnamelist=["", ""])

        if request.method == "GET":
            # 查看表单明细
            if request.GET.get('checkform'):
                h = checkform(request, usrname)
                return h
            # 返回
            elif request.GET.get('back'):
                return HttpResponseRedirect("../user/")
            # 查看用户表单列表
            else:
                userdata['formnamelist'] = myform(request, usrname)
                request.session['htmlname'] = "user.html"
                return render(request, 'user.html', userdata)
        elif request.method == "POST":
            formfileid = 1
            userdata2 = {"formnamelist": ["", ""], "formcantans": [{"itemm": "", "statuss": ""}], "selectednow": 0,
                         "fileaddres": "", "username": request.session['username']}
            # 处理历史记录查看
            if (request.POST.get("usehistory") is not None) | (
                    request.session['htmlname'] == "usehistory.html"):
                request.session['htmlname'] = "usehistory.html"
                retrundata = usehistory(request)
                return render(request, 'usehistory.html', retrundata)
            # old处理表单列表查看
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
                # 文档上传及暂存
                h2 = saveform(request, usrname)
                return h2

@check_decorate
def xuser(request):
    status = request.COOKIES.get("name")
    usrname = request.session['username']


    if (status is None) | (request.session['userkind'] != 'user'):
        return HttpResponseRedirect('../')
    else:
        userdata = dict(testloop=[""], result=[{"name": "", "size": 0}], selectnow="",
                        username=request.session['username'], formnamelist=["", ""])
        if request.method == "GET":
            # 查看表单明细
            if request.GET.get('checkform'):
                h = checkform(request, usrname)
                return h
            else:
                userdata['formnamelist'] = myform(request, usrname)
                request.session['htmlname'] = "xuser.html"
                return render(request, 'xuser.html', userdata)
        elif request.method == "POST":
            userdata2 = {"formnamelist": ["", ""], "formcantans": [{"itemm": "", "statuss": ""}], "selectednow": 0,
                         "fileaddres": "", "username": request.session['username']}
            # 处理历史记录查看
            if (request.POST.get("usehistory") is not None) | (
                    request.session['htmlname'] == "usehistory.html"):
                request.session['htmlname'] = "usehistory.html"
                retrundata = usehistory(request)
                return render(request, 'usehistory.html', retrundata)
            # 处理退出
            elif request.POST.get("quit"):
                return HttpResponseRedirect("../")
            # 处理新增
            elif request.POST.get("xform") is not None:
                request.session['htmlname'] = "xform.html"
                operationmark(usrname, "添加x表单")
                h2 = addnewform(request)
                return h2
            # 处理下载
            elif request.POST.get("filename"):
                h = downfile(request.POST.get("filename"))
                return h
            # 处理上传
            else:
                # 文档上传及暂存
                h2 = saveform(request, usrname)
                return h2



# 保存表单
def saveform(request, usrname):
    files = request.FILES.getlist('chosefiles')
    filepath = settingg()
    if request.POST.get("updatereflush"):
        upformdata(filepath, files, usrname, request.POST)
        operationmark(usrname, "updata")
        userdata = {"formfilename": "", "username": usrname,
                    "formcantain": htmlitemname(request.POST.get('formfilename')[:2], valueditem=None),
                    "readmodel": 'edit', 'uploadpermi': 'edit', "fileaddres": []}
        return render(request, request.session['htmlname'], userdata)
    else:
        h2 = addnewform(request)
        return h2


# 查看表单明细
def checkform(request, usrname):
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
    elif formbase['formfilekind'] == 'CL':
        userdata['formcantain'] = htmlitemname("CL", json.loads(formbase['formcantain']))
        request.session['htmlname'] = "job_systemchecklist.html"
        return render(request, 'job_systemchecklist.html', userdata)
    else:
        userdata['formcantain'] = htmlitemname("xl", json.loads(formbase['formcantain']))
        request.session['htmlname'] = "xform.html"
        return render(request, 'xform.html', userdata)


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
    if kind == 'xl':
        formcantainitem = {'formfilename': '', 'projectname': '', "y": 'y'}
    if valueditem is not None:
        for i in formcantainitem:
            try:
                formcantainitem[i] = valueditem[i]
            except:
                pass

    return formcantainitem

# 添加表单
def addnewform(request):
    if request.POST.get('form_fileslist'):
        shortname = "FL"
        request.session['htmlname'] = "job_fileslist.html"
    elif request.POST.get('form_syschecklist'):
        shortname = "CL"
        request.session['htmlname'] = "job_systemchecklist.html"
    else:
        try:
            shortname = request.POST.get('formfilename')[:2]
        except Exception:
            shortname='xl'

    uploader = request.session['username']
    id = 0
    try:
        id = md.formfilelist.objects.filter(uploader=uploader, formfilekind=shortname).aggregate(
            models.Max('formfileid'))['formfileid__max'] + 1
    except:
        pass
    timemark = str.replace(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d"), "_", "")
    formfilename = shortname + str(id) + "_" + timemark
    tempdata = dict(formfilename=formfilename, username=uploader, formcantain=htmlitemname(shortname), readmodel='edit',
                    uploadpermi='edit', fileaddres=[])
    return render(request, request.session['htmlname'], tempdata)


def set_cookietest(HttpResponseRedirect):
    co = HttpResponseRedirect.set_cookie("name", "coa", expires=1200)
    return co


# 用户历史记录
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


# 上传表单信息及附件
def upformdata(filepath, form, usrname, formcantain):
    formcantainstr = json.dumps(formcantain)
    # 读取基础信息
    k = int(formcantain['formfilename'][2:formcantain['formfilename'].find("_")])
    # 读取文档
    fileaddress = list()
    # 标记是否有记录
    ifesit = len(formfilelist.objects.filter(formfileid=k, uploader=usrname,
                                             formfilekind=formcantain['formfilename'][:2]).values())

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
        if formcantain['savemode'] == "update":
            filestatus = "已上传"

        else:
            filestatus = "暂存"
        if ifesit > 0:
            formfilelist.objects.filter(formfileid=k, uploader=usrname,
                                        formfilename=formcantain['formfilename']).delete()
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


# 处理模板
def checklisttemplate(request):
    request.session['templtenamelist'] = list(checklisttemplte.objects.values('templtename').iterator())
    retrundata = {"httempltename": "", 'resultlist': [["", "", ""]], 'file': "", "othinfo": ["", "", ""],
                  "namelist": request.session['templtenamelist'], "selectnow": request.POST.get("templtename")}

    # 处理查找模板
    if request.POST.get("searchtemplte"):
        templtename = request.POST.get("templteselect")
        tform = checklisttemplte.objects.filter(templtename=templtename).values()[0]
        # 返回值
        retrundata['httempltename'] = tform['templtename']
        retrundata['resultlist'] = json.loads(tform['formlist'])
        retrundata['othinfo'] = [tform['templteid'], tform['templtekind'], tform['createtime']]
        retrundata['selectnow'] = templtename
        retrundata['file'] = tform['fileaddress']
    # 处理添加模板
    elif request.POST.get("addtemplte"):
        if request.POST.get("addtempltereflush"):
            retrundata['selectnow'] = request.POST.get("templtename")
            retrundata['namelist'] = addtemplate(templtename=request.POST.get("templtename"),
                                                 templtekind=request.POST.get("templtekind"),
                                                 formlist=request.POST.get("formlist"))

        else:
            retrundata['namelist'] = list(checklisttemplte.objects.values('templtename').iterator())

    # 处理删除模板
    elif request.POST.get("deletetemplte"):
        checklisttemplte.objects.filter(templtename=request.POST.get("templteselect")).delete()
        # 更新模板名单
        retrundata['namelist'] = list(checklisttemplte.objects.values('templtename').iterator())
    return retrundata


# 处理模板-添加模板
def addtemplate(templtename, templtekind, formlist):
    k = checklisttemplte.objects.aggregate(models.Max('templteid'))['templteid__max']
    if k is None:
        k = 0
    checklisttemplte.objects.create(templteid=k + 1, templtename=templtename, templtekind=templtekind,
                                    formlist=formlist)
    templtenamelist = list(checklisttemplte.objects.values('templtename').iterator())
    return templtenamelist


# 处理模板-删除模板
def deletetemplate(templtename):
    k = checklisttemplte.objects.filter(templtename=templtename).delete()
    return None


# 读取表单列
def myform(request, name, formfilename=None):
    if formfilename is None:
        formnamelist = list(
            formfilelist.objects.filter(uploader=name).values('formfileid', 'formfilename', 'filestatus').iterator())
        return formnamelist
    else:
        formmessage = md.formfilelist.objects.filter(uploader=name, formfilename=formfilename).values()[0]
        return formmessage


# 下载表单附件
def downfile(name):
    path = settingg() + "//" + name
    re = FileResponse(open(path, 'rb'))
    re['Content-Type'] = 'application/octet-stream'
    re['Content_Disposition'] = 'attachment;filename=' + name + ''
    return re

