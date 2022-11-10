import sqlite3
# 连接数据库
# conn = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite", check_same_thread=False)
conn = sqlite3.connect(r"./instance/teachers.sqlite", check_same_thread=False)

# 使用cursor()方法获取操作游标
cursor = conn.cursor()


def sql_select_all(sql, islist=False):
    """
    查找多条数据
    :param sql:
    :param islist: 以列表形式返回
    :return:
    """
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


def sql_select(sql):
    """
    查找单条数据
    :param sql:
    :return:
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        return results
    except:
        print("Error: unable to fetch data")
        return


def sql_update(sql):
    """
    修改数据库
    :param sql:
    :return:
    """
    try:
        # 执行SQL语句
        print(sql)
        cursor.execute(sql)
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
        cursor.execute(sql)
        # 获取所有记录列表
        conn.commit()
        print('删除成功')
    except:
        print("Error: 删除失败")
        return


def sql_insert(sql):
    """
    插入数据
    :param sql:
    :return:
    """
    try:
        # 执行SQL语句
        print(sql)
        cursor.execute(sql)
        # 获取所有记录列表
        conn.commit()
        print('插入成功')
    except:
        print("Error: 插入失败")
        return
