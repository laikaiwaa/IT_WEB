from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from appa.model import userinfo,loginhistory
from django.db import connection,connections,models
import logging
mylog = logging.getLogger('myproject.custom')


#from pykafka import KafkaClient,SimpleConsumer
# broker="192.168.1.9:9092"
# broker="localhost:9092"
# k=KafkaClient(broker)
#create_topic
# topic = k.topics[b'loginhistory']
# print(topic)
#produce
# produce=topic.get_sync_producer()



def logincheck(ausername,busercode):
    result=userinfo.objects.filter(username = ausername,password=busercode).values()
    if result:
        return result[0]['type']
    else:
        return []
def loginmark(ausername):
    uid = userinfo.objects.filter(username=ausername).values()[0]['userid']
    loginhistory.objects.create(userid=uid,username=ausername)
def admincheck(ausername):
    result = userinfo.objects.filter(username=ausername).values()
    return result
def adminadd(ausername,busercode,cusertype):
    cursor=connection.cursor()
    k=cursor.execute("select count(*) from appa_userinfo").fetchall()[0][0]
    userinfo.objects.create(userid=k+1,username=ausername, password=busercode, type=cusertype)
    select = userinfo.objects.all().values()
    return select

def serch(b,e):
    cursor=connection.cursor()
    sql="select * from appa_loginhistory where  time >=datetime('"+ b +" 00:00:00.000000') " \
                    "and time <=datetime('"+ e +" 23:59:59.000000') "  \
    #sql="select * from appa_loginhistory where WHERE time >=time('"+b+ " 0:0:0') " \
    #                "and time <=time('"+e+ " 23:59:59') "  \
    l=cursor.execute(sql)
    result=l.fetchall()
    if result:
        return result

def login(request):
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    usertype= request.POST.get('usertype')
    if request.method == "GET":
        return render(request,'login.html')
    elif  request.method == "POST":
        if request.POST.get("login"):
            logic=logincheck(username, usercode)
            loginmark(username)
            # produce.produce(b'eeee')
            # produce.stop()
            if logic=='admin':
                a=HttpResponseRedirect('admin')
                set_cookietest(a)
                request.session['userkind']='adminer'
                return a
            if logic=='user':
                a=HttpResponseRedirect('use')
                set_cookietest(a)
                request.session['userkind']='user'
                return a
            else:
                return render(request, 'login.html')


def admin(request):
    status = request.COOKIES.get("name")
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    usertype= request.POST.get('usertype')
    if (status is None) | (request.session['userkind']!='adminer'):
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            return render(request, 'admin.html', {"list": [],"refrash":""})
        elif  request.method == "POST":
            if request.POST.get("check"):
                data = admincheck(username)
                return render(request, 'admin.html', {"list": data,"refrash":username})
            elif request.POST.get("add"):
                data = adminadd(username, usercode, usertype)
            return render(request, 'admin.html', {"list": data,"refrash":username})
def use(request):
    status = request.COOKIES.get("name")
    btime = request.POST.get('btime')
    etime = request.POST.get('etime')
    if (status is None) | (request.session['userkind']!='user'):
        return HttpResponseRedirect('../')
    else:
        if request.method == "GET":
            return render(request, 'use.html', {"list": [],"btime":"","etime":""})
        elif  request.method == "POST":
            if request.POST.get("serch"):
                data = serch(btime,etime)
                return render(request, 'use.html', {"list": data,"btime":btime,"etime":etime})

def set_cookietest(HttpResponseRedirect):
    co = HttpResponseRedirect.set_cookie("name","coa",expires=300)
    return co


