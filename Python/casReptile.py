import requests
from bs4 import BeautifulSoup
import pymysql
import datetime

connection = pymysql.connect(host='x.x.x.x',
                             port=3306,
                             user='root',
                             password='x',
                             db='x',
                             charset='utf8')


def get_info(url):
    wb_data = requests.get(url)  # get方法中加入请求头
	
    wb_data.encoding = 'gb2312' # 中文可能会乱码。解决方案：去要爬的网站找编码 。如： <meta http-equiv="Content-Type" content="text/html; charset=gb2312"> 
    soup = BeautifulSoup(wb_data.text, 'html.parser')  # 对返回的结果进行解析
    # soup = BeautifulSoup(wb_data.text, 'html.parser')  # 对返回的结果进行解析
    ranks = soup.select('#main > div.left.sc > div.elist > dl dd ul li')
    for t in ranks:
        text = t.get_text()
        split = text.split('(')
        enName = split[0]
        cnName = (split[1])[4:len(split[1])]
        cas = (split[2])[4:len(split[2])]
        obj = {"enName": enName, "cnName": cnName, "cas": cas}
        insert(obj)


def insert(obj):
    # 使用cursor()方法获取操作游标
    cursor = connection.cursor()
    sql = 'INSERT INTO `cas` (`cn_name`, `en_name`,`cas`) VALUES (%(cnName)s, %(enName)s ,%(cas)s)'
    try:
        # 执行sql语句
        cursor.execute(sql, obj)
        # 提交到数据库执行
        connection.commit()
    except:
        # 如果发生错误则回滚
        connection.rollback()


if __name__ == '__main__':  # 相当于java中的main方法
    startTime = datetime.datetime.now()
    chars = map(chr, range(ord('a'), ord('z') + 1))
    for a in chars:
        url = 'http://china.chemnet.com/hot-product/{}.html'.format(a)
        get_info(url)
    # 关闭数据库连接
    connection.close()
    endTime = datetime.datetime.now()
    print((endTime - startTime).seconds)
