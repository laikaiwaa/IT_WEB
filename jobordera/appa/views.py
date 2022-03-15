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


cursor=connection.cursor()
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
    k=cursor.execute("select count(*) from django2_userinfo").fetchall()[0][0]
    userinfo.objects.create(userid=k+1,username=ausername, password=busercode, type=cusertype)
    select = userinfo.objects.all().values()
    return select

def serch(b,e):
    sql="select day,weixintimes,cardtimes,sumtimes,round(weixintimes/sumtimes,2)  as weixinrate from "\
                "("\
                "select day,sum(case when type='微信注册会员' then times else 0 end) as weixintimes ,"\
                "sum(case when type='微信绑定实体' then times else 0 end) as cardtimes,"\
                "sum(times) as sumtimes "\
                    "from weixinbindtrend "\
                    "WHERE DAY >=TO_DATE('"+b+ " 0:0:0','yyyy-MM-dd HH24:mi:ss') " \
                    "and DAY <=TO_DATE('"+e+ " 23:59:59','yyyy-MM-dd HH24:mi:ss') "  \
                    "group by day " \
                    "order by day" \
                ") "
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
                return HttpResponseRedirect('admin')
            if logic=='user':
                return HttpResponseRedirect('use')
            else:
                return render(request, 'login.html')


def admin(request):
    username = request.POST.get('username')
    usercode = request.POST.get('usercode')
    usertype= request.POST.get('usertype')
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
    btime = request.POST.get('btime')
    etime = request.POST.get('etime')
    if request.method == "GET":
        return render(request, 'use.html', {"list": [],"btime":"","etime":""})
    elif  request.method == "POST":
        if request.POST.get("serch"):
            data = serch(btime,etime)
            return render(request, 'use.html', {"list": data,"btime":btime,"etime":etime})

import logging


