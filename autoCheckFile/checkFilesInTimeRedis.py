#!/usr/bin/python
# coding=utf-8
'''
@ctime: 2017年3月24日
@author: Bellpost
'''
#检查主机目录下的文件

import smtplib,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import dealconfig
import redis
import hashlib
from datetime import datetime
from fabric.api import *
from fabric.contrib.files import exists
import time,logging,datetime


logger = logging.getLogger()
fh = logging.FileHandler('fileexits.log')
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.ERROR)

config_file_path="./conf/config.ini"
dealconfig = dealconfig(config_file_path)

redisHost = dealconfig.get("redis", "host")
Port = dealconfig.get("redis", "port")
db = dealconfig.get("redis", "db")
HOST = dealconfig.get("email", "HOST")
FROM = dealconfig.get("email", "FROM")
TO = dealconfig.get("email", "TO").split(',')

r=redis.Redis(host=redisHost,port=Port,db=db)

env.user = 'user'
env.roledefs = {
    'sjgt': [''],
    'GPS': ['']
    }
env.passwords = {
    'user@ip:22':'passwd'
    }
env.hosts = ['']


busGpsHour = "/data/GPS/"
TaxiGpsHour = "/data/GPS/"
STLPath = "/data/GPS"


date_title = time.strftime('%Y%m%d %H:%M')
SUBJECT = u"<Auto>数据生成告警 Time："+date_title



def nowtime():
    return time.strftime('%Y%m%d %H:%M:%S')

def get5Min():
    # (datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M")
    min = int((datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime("%M"))
    if min == 0:
        MM = "00"
    else:
        MM = min - min % 5
        if MM <= 9:
            MM = "0" + str(MM)
    return (datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%Y%m%d%H') + str(MM)

def get15Min():
    min = int((datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%M'))
    if min == 0:
        MM = "00"
    else:
        MM = min - min % 15
        if MM == 0:
            MM = "00"
    return (datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%Y%m%d%H') + str(MM)

def getHour():
    return (datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%Y%m%d%H')

def getDelayHour(delaytime):
    return (datetime.datetime.now() - datetime.timedelta(hours=delaytime)).strftime('%Y%m%d%H')

def getOnlyHour():
    return (datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%H')

def getOnlyDelayHour(delaytime):
    return (datetime.datetime.now() - datetime.timedelta(hours=delaytime)).strftime('%H')
def getDay():
    return (datetime.datetime.now() - datetime.timedelta(hours=0.25)).strftime('%Y%m%d')

def getZYDDay():
    if int(datetime.datetime.now().strftime('%H')) >= 12:
        return datetime.datetime.now().strftime('%Y%m%d')
    else:
        return (datetime.datetime.now() - datetime.timedelta(days=0.5)).strftime('%Y%m%d')

def write_csv(role,path):
    with open('/data/GPS_DATA/path.csv','a+') as f :
        if role=='GPS':
            row=str('IP,服务,'+'计算结果'+','+time.strftime('%Y-%m-%d')+','+'文件未生成,'+'异常'+path+'\n')
            f.write(row)
        elif role == 'sjgt':
            row = str('IP,服务,' + '文件' + ',' + time.strftime('%Y-%m-%d') + ',' + '文件未生成,' + '异常' + path+'\n')
            f.write(row)
        else:
            pass

def getFilePath(Path):
    md5 = hashlib.md5()
    md5.update(bytes(Path))
    md5PathValue = md5.hexdigest()
    newPath = r.get(md5PathValue)
    if newPath is None :
        r.set(md5PathValue, Path)
        return Path
    else:
        return None

def mail_cont(cont):
    mailcont = ""
    for i in cont :            
        mailcont = mailcont + "<p><font color=red>[WARN]: 数据未生成  目录为["+i+"] </font></p>"
    msg = MIMEMultipart('related')
    msgtext = MIMEText(mailcont,"html","utf-8")
    msg.attach(msgtext)
    msg['Subject'] = SUBJECT
    msg['From']=FROM
    #msg['To']=TO
    return msg

def sendMail(msg,role):
    i = 0
    while True:
        try:
            server = smtplib.SMTP()
            server.connect(HOST,"25")
            server.login("-@139.com","")
            for to_user in TO:
                server.sendmail(FROM, to_user, msg.as_string())
                logging.error(nowtime()+":Role:[" +role+ "]: Email send ["+to_user+"] Successful!" )
            server.quit()
            break
        except Exception, e:  
            i=i+1
            logging.error(nowtime()+":Role:[" +role+ "]: Email send failed:"+str(e) )
            if i<=3:
                continue
            else:
                sys.exit(0)
        

@roles('GPS143')
def fileExits143():
    role = "GPS143"
    busGpsHourPath = busGpsHour +getDay() + "/" + getOnlyHour() +".csv"
    TaxiGpsHourPath = TaxiGpsHour +getDay() + "/" + getOnlyHour() +".csv"
    allPath = [busGpsHourPath,TaxiGpsHourPath]
    conts=[]
    for i in allPath:
        pathRes = getFilePath(i)
        if pathRes is not None:
            if not exists(pathRes):
                conts.append(pathRes)
    if conts is not None:
        for file in conts:
            write_csv(role,file)
    return conts,role


@roles('sjgt')
def fileExits148():
    role = "sjgt"
    STLPath = STLRootPath + getDay() + "/"+get5Min()+".csv"
    allPath = [STLPath]
    conts=[]
    for i in allPath:
        pathRes = getFilePath(i)
        if pathRes is not None:
            if not exists(pathRes):
                conts.append(pathRes)
    if conts is not None:
        for file in conts:
            write_csv(role,file)
    return conts,role

@task
@roles('GPS')
def go143():
    role = 'GPS'
    try:
        cont143,role = fileExits143()
        if cont143:
            msg = mail_cont(cont143)
            sendMail(msg,role)
        elif not cont143:
            logging.error(nowtime()+":Role: [" +role+ "]: Files is normal" )     
    except Exception, e:  
        logging.error(nowtime()+ ":Role:[" +role+ "] Fabric run Error "+str(e))
        sys.exit(0)


@task
@roles('sjgt')
def go148():
    role = 'sjgt'
    try:
        cont148,role = fileExits148()
        if cont148:
            msg = mail_cont(cont148)
            sendMail(msg,role)
        elif not cont148:
            logging.error(nowtime()+":Role:[" +role+ "]: Files is normal" )  
    except Exception, e:  
        logging.error(nowtime()+ ":Role:[" +role+ "]: Fabric run Error "+str(e))
        sys.exit(0)
