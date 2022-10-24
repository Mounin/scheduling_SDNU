import pandas as pd
from src.schedule import Schedule
from src.teachers_list import teacher_select

# 读入文件并转化为列表
f_path = '../data/teachers7.xlsx'
name_list_input = pd.read_excel(f_path, index_col=0, usecols=[0])
name_list_input.replace('\s+', '', regex=True, inplace=True)  # 忽略空格

class CQShifts:
    num_weekday = 13
    num_weekday_night = 48
    num_weekend = 5
    num_weekend_night = 16
    num_all_teachers = num_weekday + num_weekday_night + num_weekend + num_weekend_night


class QFSShifts:
    num_weekday = 10
    num_weekday_night = 30
    num_weekend = 4
    num_weekend_night = 10
    num_all_teachers = num_weekday + num_weekday_night + num_weekend + num_weekend_night


cq_shift = CQShifts
qfs_shift = QFSShifts

# 保证两校区数量都足够
while True:
    cq_name_list = teacher_select(name_list_input, 'cq', cq_shift.num_all_teachers)
    qfs_name_list = teacher_select(name_list_input, 'qfs', qfs_shift.num_all_teachers, cq_name_list)
    if qfs_shift.num_all_teachers >= len(name_list_input) - cq_shift.num_all_teachers:
        break

if __name__ == '__main__':
    # for i in range(50):
    #     schedule = Schedule(name_list, num_weekday, num_weekday_night, num_weekend, num_weekend_night)
    #     print("*"*50, f'第{i+1}轮结束', "*"*50)

    cq_schedule = Schedule('长清湖校区', cq_name_list, CQShifts)
    qfs_schedule = Schedule('千佛山校区', qfs_name_list, QFSShifts)

