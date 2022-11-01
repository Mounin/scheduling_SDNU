import sqlite3
# 连接数据库
conn = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite", check_same_thread=False)

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

def sql_select(sql, islist=False):
    try:
        # 执行SQL语句
        # cursor.execute(sql)
        cursor.execute("SELECT * FROM teachers")
        # 获取所有记录列表
        results = cursor.fetchall()
        conn.close()
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


def sql_update(sql):
    """
    修改数据库
    :param sql:
    :return:
    """
    try:
        # 执行SQL语句
        print('11', sql)
        cursor.execute(sql)
        print('22', sql)
        # 获取所有记录列表
        conn.commit()
        print('更新成功')
    except:
        print("Error: 更新失败")
        return


def sql_delete(sql):
    """
    修改数据库
    :param sql:
    :return:
    """
    try:
        # 执行SQL语句
        print('11', sql)
        cursor.execute(sql)
        print('22', sql)
        # 获取所有记录列表
        conn.commit()
        print('删除成功')
    except:
        print("Error: 删除失败")
        return