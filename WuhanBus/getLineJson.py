#encoding=utf-8
#-*- coding:utf-8 -*-
import urllib
import urllib2
import json
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

conn = sqlite3.connect('whbus.db')
cursor = conn.cursor()

# 创建表
cursor.execute("CREATE TABLE whbusinfo ( lineId varchar(20,0) NOT NULL,  lineNo varchar(10,0),  \
	 lineName varchar(10,0), direction int, endStopName varchar(64,0), \
	 startStopName varchar(64,0),firstTime varchar(10,0), lastTime varchar(10,0),\
	 stopsNum int, PRIMARY KEY(lineId))" )
# 创建表
cursor.execute("CREATE TABLE whbusstationinfo (lineId varchar(20,0),lineNo varchar(10,0),\
	 stopId varchar(20,0), stopName varchar(64,0), stopNo varchar(20,0),\
	 jingdu DECIMAL(3,12),weidu DECIMAL(3,12), orderId int )" )

def getJson(url):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    req = urllib2.Request(URL, headers=headers)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def mian():
    lineSQL='INSERT INTO "main"."whbusinfo" ("lineId", "lineNo", "lineName", "direction", "endStopName", \
                  "startStopName", "firstTime", "lastTime", "stopsNum") values(?,?,?,?,?,?,?,?,?)'
    stationSQL='insert into "main"."whbusstationinfo" ( "lineId", "lineNo", "stopId", "stopName", \
                  "stopNo", "jingdu", "weidu", "orderId") values ( ?, ?, ?, ?, ?, ?, ?, ?)'
    for lineNo in range(1,1000):
        print lineNo
        for direction in ['0','1']:
            URL = "http://www.wbus.cn/getQueryServlet?Type=LineDetail&lineNo=%s&direction=%s" % (lineNo,direction)
            s=getJson(URL)
            if s.keys is not None:
                if s['resultCode'] and s['resultCode']=='1':
                    lineId = s['data']['line']['lineId']
                    lineNo = s['data']['line']['lineNo']
                    lineName = s['data']['line']['lineName']
                    direction = s['data']['line']['direction']
                    endStopName = s['data']['line']['endStopName']
                    startStopName = s['data']['line']['startStopName']
                    firstTime = s['data']['line']['firstTime']
                    lastTime = s['data']['line']['lastTime']
                    stopsNum = s['data']['line']['stopsNum']
                    lineparms=[lineId, lineNo, lineName, direction, endStopName, startStopName,
                                firstTime, lastTime, stopsNum]
                    cursor.execute(lineSQL, lineparms)

                    for orderId in range(0,len(s['data']['stops'])):
                        stopId = s['data']['stops'][orderId]['stopId']
                        stopName = s['data']['stops'][orderId]['stopName']
                        stopNo = s['data']['stops'][orderId]['stopNo']
                        jingdu = s['data']['stops'][orderId]['jingdu']
                        weidu = s['data']['stops'][orderId]['weidu']
                        stationparms = [lineId, lineNo, stopId, stopName ,stopNo, jingdu, weidu ,orderId]
                        cursor.execute(stationSQL,stationparms)
        conn.commit()
        cursor.close()


if __name__ == '__main__':
    mian()



