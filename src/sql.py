import pymysql
# 连接数据库
db = pymysql.connect(host='localhost',
                     user='root',
                     password='lemon',
                     database='sdnu_schedule')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

def sql_select(sql, islist=False):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if islist:
            datalist = []
            alldata = results
            for i in alldata:
                datalist.append(i[0])
            return datalist
        else:
            return results
    except:
        print("Error: unable to fetch data")
        return