import os
import sqlite3
import time

import pandas as pd
import numpy as np

from src.sql import sql_select_all, sql_select

# 连接数据库
db = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite", check_same_thread=False)

# 使用cursor()方法获取操作游标
cursor = db.cursor()


def compare():
    # 读取数据库一列数据
    sql = "SELECT num_weekday,num_weekday_night, num_weekend, num_weekend_night FROM teachers"
    cursor.execute(sql)
    datalist = []
    alldata = cursor.fetchall()
    threshold = np.zeros(4)

    for j in range(4):
        for i in alldata:
            datalist.append(i[j])
        threshold[j] = np.max(datalist) * 0.7
        datalist = []
    return threshold


class Schedule:
    def __init__(self, school, name_list, shift):
        """
        1. 对数据预处理
        :param name_list: 导入的名单
        """

        self.name_list = name_list
        self.school = school
        self.weekday = []
        self.weekday_night = []
        self.weekend = []
        self.weekend_night = []
        print("待分配人员数量：", len(self.name_list))
        # 休息日晚上工作人员
        self.weekend_or_night_schdule('weekend_night', shift.num_weekend_night)
        # # 休息日白天工作人员
        self.weekend_or_night_schdule('weekend', shift.num_weekend)
        # # 工作日晚上工作人员
        self.weekday_or_night_schedule('weekday_night', shift.num_weekday_night)
        # # 工作日白天工作人员
        self.weekday_or_night_schedule('weekday', shift.num_weekday)
        # 合并到一起
        self.result_path = self.schedule_concat()

    def weekend_or_night_schdule(self, time, num):
        """
        分配休息日白天或者休息日晚上值班
        :param time: 值班时间
        :param num: 值班人数
        """
        _name_list = self.name_list
        threshold = compare()
        for teacher in _name_list.index:
            # SQL 查询语句
            sql = "SELECT * FROM teachers WHERE name='%s'" % (teacher)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
                for result in results:
                    # 如果上一次在周末值班，则本次不安排在周末
                    if result[1] == "休息日白天" or result[1] == "休息日晚上":
                        _name_list = _name_list.drop(teacher)
            except:
                print("Error: unable to fetch data")

        if time == 'weekend_night':
            for row in _name_list.iterrows():
                name = row[0].replace(' ', '')
                select_sql = f"SELECT num_weekend_night FROM teachers WHERE name='{name}'"
                numm = sql_select(select_sql)
                if numm >= threshold[3]:
                    _name_list = _name_list.drop(name)
            self.weekend_night = _name_list.sample(num)
            _df = self.weekend_night
        if time == 'weekend':
            for row in _name_list.iterrows():
                name = row[0].replace(' ', '')
                select_sql = f"SELECT num_weekend FROM teachers WHERE name='{name}'"
                numm = sql_select(select_sql)
                if numm >= threshold[3]:
                    _name_list = _name_list.drop(name)
            self.weekend = _name_list.sample(num)
            _df = self.weekend
        self.name_list = self.name_list.drop(_df.index)
        print(f'分配完{time}后剩余人员数量：', len(self.name_list))

    def weekday_or_night_schedule(self, time, num):
        """
        分配工作日白天或者工作日晚上值班
        :param time: 值班时间
        :param num: 值班人数
        """
        _name_list = self.name_list
        threshold = compare()
        if time == 'weekday':
            self.weekday = _name_list.sample(num)
            _df = self.weekday
        if time == 'weekday_night':
            for row in _name_list.iterrows():
                name = row[0].replace(' ', '')
                select_sql = f"SELECT num_weekday_night FROM teachers WHERE name='{name}'"
                numm = sql_select(select_sql)
                if numm >= threshold[1]:
                    _name_list = _name_list.drop(name)
                    print('&' * 80, name, len(_name_list))
            self.weekday_night = _name_list.sample(num)
            _df = self.weekday_night
        self.name_list = self.name_list.drop(_df.index)
        print(f'分配完{time}后剩余人员数量：', len(self.name_list))

        print(threshold)

    def schedule_concat(self):
        """
        合成一张表格
        :return: 合并在一起的表格
        """
        # 只保留名字一列
        _weekday = self.weekday
        _weekday_night = self.weekday_night
        _weekend = self.weekend
        _weekend_night = self.weekend_night

        result_list = [_weekday, _weekday_night, _weekend, _weekend_night]
        result = pd.concat(result_list, keys=['工作日白天', '工作日晚上', '休息日白天', '休息日晚上'])
        # 输出excel

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        #######################################
        # 毫秒级时间戳
        file_name = f"{self.school}"
        dir = str(time.strftime('%y%m%d', time.localtime()))
        out_path = os.path.join(basepath, 'output/' + dir)
        # 判断文件夹是否存在
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        #######################################
        file_path = str(file_name)
        f_path = out_path + '/' + file_path + '.xlsx'
        result.to_excel(f_path)
        return f_path







