import numpy as np
import pandas as pd

from src.sql import sql_update, sql_delete, sql_select, sql_insert


# 更新teacher信息
def update_teacher(teacher):
    teacher_id = teacher['id']
    for key in teacher:
        if key == 'cq':
            if teacher[key] == '是':
                teacher[key] = True
            elif teacher[key] == '否':
                teacher[key] = False
        elif key == 'qfs':
            if teacher[key] == '是':
                teacher[key] = True
            elif teacher[key] == '否':
                teacher[key] = False
        sql = f"UPDATE teachers SET {key}={teacher[key]} WHERE id={teacher_id}"
        sql_update(sql)


def delete_teacher(tid):
    """
    删除teacher
    :param tid:
    :return:
    """
    sql = f'DELETE FROM teachers WHERE id={tid}'
    sql_delete(sql)


def update_teacher_database(f_path):
    """
    更新数据库
    :param f_path: 文件路径
    :return:
    """
    f_path = f_path['f_path']
    name_list = pd.read_excel(f_path, index_col=0)
    name_list.replace('\s+', '', regex=True, inplace=True)  # 忽略空格
    for index, row in name_list.iterrows():
        name = str(index)
        name = name.replace(' ', '')
        last_status = row.values[0]
        num_weekday = row.values[1]
        num_weekday_night = row.values[2]
        num_weekend = int(row.values[3])
        num_weekend_night = int(row.values[4])
        select_sql = f"SELECT * FROM teachers WHERE name='{name}'"
        is_None = sql_select(select_sql)
        if is_None is None:
            insert_sql = f"INSERT INTO teachers (name, last_status, num_weekday, num_weekday_night, num_weekend, num_weekend_night, cq, qfs)" \
                         f"VALUES ('{name}', '{last_status}', {num_weekday}, {num_weekday_night}, {num_weekend}, {num_weekend_night}, 0, 0)"
            sql_insert(insert_sql)
        else:
            update_sql = f"UPDATE teachers SET last_status='{last_status}'," \
                     f"num_weekday=num_weekday+{num_weekday}," \
                     f"num_weekday_night=num_weekday_night+{num_weekday_night}," \
                     f"num_weekend=num_weekend+{num_weekend}," \
                     f"num_weekend_night=num_weekend_night+{num_weekend_night}  WHERE name='{name}'"
            sql_update(update_sql)


def check_database(f_path):
    """
    检查数据库中是否存在老师，并检查cq和qfs状态
    :return:
    """
    f_path = f_path['f_path']
    df = pd.read_excel(f_path)
    for index, teacher in df.iterrows():
        name = teacher['name'].replace(' ', '')
        select_sql = f"SELECT * FROM teachers WHERE name='{name}'"
        result = sql_select(select_sql)
        if result is None:
            insert_sql = f"INSERT INTO teachers (name, num_weekday, num_weekday_night, num_weekend, num_weekend_night, cq, qfs)" \
                         f"VALUES ('{name}', 0, 0, 0, 0, {teacher['cq']}, {teacher['qfs']})"
            sql_insert(insert_sql)
        else:
            update_sql = f"UPDATE teachers SET cq={teacher['cq']}, qfs={teacher['qfs']} WHERE name='{name}'"
            sql_update(update_sql)
