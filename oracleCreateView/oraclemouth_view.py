#coding=utf-8
import cx_Oracle                                          #引用模块cx_Oracle
import logging,time
from config import dealconfig

mtime="select to_char(sysdate,'yyyyMM') from dual"


logger = logging.getLogger()
fh = logging.FileHandler('CreateView.log')
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.ERROR)

config_file_path="./conf/config.ini"
dealconfig = dealconfig(config_file_path)



def nowtime():
    return time.strftime('%Y%m%d %H:%M:%S')


#获取oracle数据库当前时间
def getOracleTime(timesql):
    res=c.execute(timesql)
    restime=res.fetchone()
    if restime is not None:
        return restime
    else:
        return None
#替换视图
def replaceView(viewname,tablename,montime): 
    if montime is None:
        logging.error(nowtime()+": Get ORACLE Time Error")
        sys.exit(1)
    judgeTable="SELECT COUNT(1) FROM USER_TABLES WHERE table_name = '%s'" %(tablename)
    logging.error(nowtime()+": "+judgeTable)
    jugRes=c.execute(judgeTable).fetchone()
    if isinstance(jugRes[0],int):
        if jugRes[0]==1:
            dropViewSql="create or replace view %s as select * from %s " %(viewname, tablename)
            logging.error(nowtime()+": "+dropViewSql)
            c.execute(dropViewSql)
        else:
            logging.error(nowtime()+": Table not exists")

        
def main():
    table_list=dealconfig.get("baseconf","table_list").split(',')
    table_list_th=dealconfig.get("baseconf","table_list_th").split(',')
    table_list_wh=dealconfig.get("baseconf","table_list_wh").split(',')

    for onetable in table_list:
        montime=getOracleTime(mtime)
        temp_montime= dealconfig.get("table_list",onetable+"_montime")
        if temp_montime!=montime[0]:
            tablename=onetable+montime[0]
            replaceView(onetable,tablename,montime)
            dealconfig.set("table_list",onetable+"_montime",montime[0])
        else:
            logging.error(nowtime()+": TableView is Created ; TableViewName: "+onetable)

            
    for onetable in table_list_th:
        tail="_TH"
        montime=getOracleTime(mtime)
        temp_montime= dealconfig.get("table_list_th",onetable+tail+"_montime")
        if temp_montime!=montime[0]:
            tablename=onetable+montime[0]+tail
            replaceView(onetable+tail,tablename,montime)
            dealconfig.set("table_list_th",onetable+tail+"_montime",montime[0])
        else:
            logging.error(nowtime()+": TableView is Created ; TableViewName: "+onetable+tail)

    for onetable in table_list_wh:
        tail="_WH"
        montime=getOracleTime(mtime)
        temp_montime= dealconfig.get("table_list_wh",onetable+tail+"_montime")
        if temp_montime!=montime[0]:
            tablename=onetable+montime[0]+tail
            replaceView(onetable+tail,tablename,montime)
            dealconfig.set("table_list_wh",onetable+tail+"_montime",montime[0])
        else:
            logging.error(nowtime()+": TableView is Created ; TableViewName: "+onetable+tail)

if __name__=='__main__':    
    conn=cx_Oracle.connect(dealconfig.get("oracle","connect"))    #连接数据库
    c=conn.cursor()
    main()
    c.close()  #关闭cursor
    conn.close()
