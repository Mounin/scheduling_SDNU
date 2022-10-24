import pymysql
import pandas as pd
import sql
# 连接数据库
db = pymysql.connect(host='localhost',
                     user='root',
                     password='lemon',
                     database='sdnu_schedule')

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
        print("进来了吗"*50)
        add_teachers = []
        print(type(add_teachers))
        for teacher in name_list.index:
            is_qfs = sql.sql_select(f'SELECT qfs FROM teachers WHERE name="%s"' % (teacher), islist=True)
            print(teacher, '*' * 20, is_qfs)
            if is_qfs[0] == 1:
                add_teachers.append(teacher)
                print('&'*10, add_teachers)

    if school == 'cq':
        add_teachers = []
        print(type(add_teachers))
        for teacher in name_list.index:
            is_cq = sql.sql_select(f'SELECT cq FROM teachers WHERE name="%s"' % (teacher), islist=True)
            print(teacher, '*' * 20, is_cq)
            if is_cq[0] == 1:
                add_teachers.append(teacher)
                print('&'*10, len(add_teachers))

    # add_teachers = sql.sql_select(f'SELECT name FROM teachers WHERE {"qfs" if school == "qfs" else "cq"}=1',
    #                       islist=True)

    output_name_list = pd.DataFrame(add_teachers, columns=['name']).set_index('name')

    # 将已经在输出列表中的老师从总表中删除
    for teacher in output_name_list.index:
        if teacher in name_list.index:
            name_list = name_list.drop(teacher)

    # 将条件必须不在该校区值班的老师删除
    drop_teachers = sql.sql_select(f'SELECT name FROM teachers WHERE {"cq" if school=="qfs" else "qfs"}=1', islist=True)
    for teacher in drop_teachers:
        if teacher in name_list.index:
            name_list = name_list.drop(teacher)

    # 在总表中随机选出num - len(add_teachers)个老师
    name_list = name_list.sample(num - len(add_teachers))
    # 将name_list和必须在该校值班的表合并
    output_name_list = pd.concat([name_list, output_name_list], axis=1)  # axis=0：纵向合并
    return output_name_list
