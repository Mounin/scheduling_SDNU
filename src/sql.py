import sqlite3

import pymysql
# 连接数据库
conn = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite")

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

def sql_select(sql, islist=False):
    try:
        # 执行SQL语句
        print('&*'*50, sql)
        # cursor.execute(sql)
        cursor.execute("SELECT * FROM teachers")
        print('&*' * 50, 123321)
        # 获取所有记录列表
        results = cursor.fetchall()
        conn.close()
        print('&*'*50, results)
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
        conn.close()
        return