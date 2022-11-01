from src.sql import sql_update, sql_delete


# 更新teacher信息
def update_teacher(teacher):
    teacher_id = teacher['id']
    for key in teacher:
        # print(key, teacherDetail[key])
        if key == 'last_status':
            if teacher[key] == '工作日白天':
                teacher[key] = 'weekday'
            elif teacher[key] == '工作日晚上':
                teacher[key] = 'weekday_night'
            elif teacher[key] == '休息日白天':
                teacher[key] = 'weekend'
            elif teacher[key] == '休息日晚上':
                teacher[key] = 'weekend_night'
        elif key == 'cq':
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


# 删除teacher
def delete_teacher(tid):
    sql = f'DELETE FROM teachers WHERE id={tid}'
    sql_delete(sql)
