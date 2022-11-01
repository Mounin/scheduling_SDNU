import pandas as pd
import sqlite3
# 连接数据库
db = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite", check_same_thread=False)

# 使用cursor()方法获取操作游标
cursor = db.cursor()


def teacher_select(name_list, school, num, selected_list=pd.DataFrame()):
    """
    选择两个校区的老师
    :param name_list: 老师列表
    :param school: 校区
    :param num: 校区需要的数量
    :param selected_list: 已经选择分配完的老师列表
    :return: 该校区的老师列表
    """
    # 如果有老师已经分配，则从老师列表中去除（保证老师不重复）
    if len(selected_list) != 0:
        name_list = name_list.drop(selected_list.index)

    # 将必须在该校区的老师加入输出列表

    if school == 'qfs':
        print("进来了吗11111111111111111111111111111111111111111111111")
        add_teachers = []
        for teacher in name_list.index:
            my_sql = "SELECT qfs FROM teachers WHERE name='%s'" % (teacher)
            # is_qfs = sql_select(my_sql, islist=True)
            cursor.execute(my_sql)
            is_qfs = cursor.fetchall()
            print(teacher, '*' * 20, is_qfs[0][0])
            if is_qfs[0][0] == 1:
                add_teachers.append(teacher)

    if school == 'cq':
        add_teachers = []
        for teacher in name_list.index:
            my_sql = "SELECT cq FROM teachers WHERE name='%s'" % (teacher)
            # is_cq = sql_select(my_sql, islist=True)
            cursor.execute(my_sql)
            is_cq = cursor.fetchall()
            print(teacher, '*' * 20, is_cq[0][0])
            if is_cq[0][0] == 1:
                add_teachers.append(teacher)

    output_name_list = pd.DataFrame(add_teachers, columns=['name']).set_index('name')
    print('&' * 50, output_name_list, len(output_name_list))

    # 将已经在输出列表中的老师从总表中/删除
    for teacher in output_name_list.index:
        if teacher in name_list.index:
            name_list = name_list.drop(teacher)

    # 将条件必须不在该校区值班的老师删除
    my_sql = f'SELECT name FROM teachers WHERE {"cq" if school=="qfs" else "qfs"}=1'
    # drop_teachers = sql_select(f'SELECT name FROM teachers WHERE {"cq" if school=="qfs" else "qfs"}=1', islist=True)
    cursor.execute(my_sql)
    drop_teachers = cursor.fetchall()

    for teacher in drop_teachers:
        if teacher[0] in name_list.index:
            name_list = name_list.drop(teacher[0])
    print(name_list, len(name_list), num, type(num))

    # 在总表中随机选出num - len(add_teachers)个老师
    name_list = name_list.sample(num - len(add_teachers))
    # 将name_list和必须在该校值班的表合并
    output_name_list = pd.concat([name_list, output_name_list], axis=1)  # axis=0：纵向合并
    return output_name_list


