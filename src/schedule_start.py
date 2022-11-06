import pandas as pd
from src.schedule import Schedule
from src.teachers_list import teacher_select


class CQShifts:
    def __init__(self, num_weekday, num_weekday_night, num_weekend, num_weekend_night):
        self.num_weekday = num_weekday
        self.num_weekday_night = num_weekday_night
        self.num_weekend = num_weekend
        self.num_weekend_night = num_weekend_night
        self.num_all_teachers = num_weekday + num_weekday_night + num_weekend + num_weekend_night


class QFSShifts:
    def __int__(self, num_weekday, num_weekday_night, num_weekend, num_weekend_night):
        self.num_weekday = num_weekday
        self.num_weekday_night = num_weekday_night
        self.num_weekend = num_weekend
        self.num_weekend_night = num_weekend_night
        self.num_all_teachers = self.num_weekday + self.num_weekday_night + self.num_weekend + self.num_weekend_night


def schedule_start(params):
    # 读入文件并转化为列表
    f_path = params.get('f_path')
    name_list_input = pd.read_excel(f_path, index_col=0, usecols=[0])
    name_list_input.replace('\s+', '', regex=True, inplace=True)  # 忽略空格

    cq_num_weekday = int(params.get('cq_num_weekday'))
    cq_num_weekday_night = int(params.get('cq_num_weekday_night'))
    cq_num_weekend = int(params.get('cq_num_weekend'))
    cq_num_weekend_night = int(params.get('cq_num_weekend_night'))
    cq_shift = CQShifts(cq_num_weekday, cq_num_weekday_night, cq_num_weekend, cq_num_weekend_night)

    qfs_num_weekday = int(params.get('qfs_num_weekday'))
    qfs_num_weekday_night = int(params.get('qfs_num_weekday_night'))
    qfs_num_weekend = int(params.get('qfs_num_weekend'))
    qfs_num_weekend_night = int(params.get('qfs_num_weekend_night'))
    qfs_shift = CQShifts(qfs_num_weekday, qfs_num_weekday_night, qfs_num_weekend, qfs_num_weekend_night)


    # 保证两校区数量都足够
    while True:
        cq_name_list = teacher_select(name_list_input, 'cq', cq_shift.num_all_teachers)
        qfs_name_list = teacher_select(name_list_input, 'qfs', qfs_shift.num_all_teachers, cq_name_list)
        if qfs_shift.num_all_teachers >= len(name_list_input) - cq_shift.num_all_teachers:
            break

    cq_schedule = Schedule('长清湖校区', cq_name_list, cq_shift)
    qfs_schedule = Schedule('千佛山校区', qfs_name_list, qfs_shift)
    return cq_schedule.result_path, qfs_schedule.result_path

