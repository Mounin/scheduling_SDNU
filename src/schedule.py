import os
import sqlite3
import time

import pandas as pd
import numpy as np


# 连接数据库
db = sqlite3.connect("E:\\workspace\\scheduling_SDNU\\instance\\teachers.sqlite", check_same_thread=False)

# 使用cursor()方法获取操作游标
cursor = db.cursor()


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
        # # 工作日白天工作人员
        self.weekday_or_night_schedule('weekday', shift.num_weekday)
        # # 工作日晚上工作人员
        self.weekday_or_night_schedule('weekday_night', shift.num_weekday_night)
        # 合并到一起
        self.schedule_concat()

        self.variance()

    def weekend_or_night_schdule(self, time, num):
        """
        分配休息日白天或者休息日晚上值班
        :param time: 值班时间
        :param num: 值班人数
        """
        _name_list = self.name_list
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
                    if result[1] == "weekend" or result[1] == "weekend_night":
                        _name_list = _name_list.drop(teacher)

            except:
                print("Error: unable to fetch data")

        # 选出该时间段值班次数最多的老师
        # num_weekdend_night = 'num_weekend_night'
        # num_weekdend = 'num_weekend'
        # if time == 'weekend_night':
        #     _i = 3
        # else:
        #     _i = 2
        # for i in range(_i):
        #     sql = f"SELECT {num_weekdend_night if time == 'weekend_night' else num_weekdend} FROM teachers"
        #     datalist = []
        #     alldata = self.sql_select(sql)
        #     for i in alldata:
        #         datalist.append(i[0])
        #     num_max = np.max(datalist)
        #     sql = f"SELECT name FROM teachers WHERE {num_weekdend_night if time == 'weekend_night' else num_weekdend}={num_max}"
        #     teacher = self.sql_select(sql)
        #     # 每次drop一个人出去
        #     print("前", len(_name_list))
        #     for name in _name_list.index:
        #         if teacher[0][0] == name:
        #             _name_list = _name_list.drop(teacher[0][0])
        #     print("后", len(_name_list))

        if time == 'weekend_night':
            self.weekend_night = _name_list.sample(num)
            _df = self.weekend_night
        if time == 'weekend':
            self.weekend = _name_list.sample(num)
            _df = self.weekend
        # 修改数据库中的；last_status字段为weekend_night
        for teacher in _df.index:
            # SQL 更新上一次值班事件和值班次数
            if time == 'weekend_night':
                sql = "UPDATE teachers SET last_status='%s', num_weekend_night=num_weekend_night+1 WHERE name='%s'" % (time, teacher)
            if time == 'weekend':
                sql = "UPDATE teachers SET last_status='%s', num_weekend=num_weekend+1 WHERE name='%s'" % (time, teacher)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                # print("修改成功")
            except:
                # 发生错误时回滚
                db.rollback()
                # print("修改失败")
        self.name_list = self.name_list.drop(_df.index)
        print(f'分配完{time}后剩余人员数量：', len(self.name_list))

    def weekday_or_night_schedule(self, time, num):
        """
        分配工作日白天或者工作日晚上值班
        :param time: 值班时间
        :param num: 值班人数
        """
        _name_list = self.name_list
        if time == 'weekday':
            self.weekday = _name_list.sample(num)
            _df = self.weekday
        if time == 'weekday_night':
            self.weekday_night = _name_list.sample(num)
            _df = self.weekday_night
        # 修改数据库中的；last_status字段为weekday
        for teacher in _df.index:
            # SQL 更新上一次值班事件和值班次数
            if time == 'weekday':
                sql = "UPDATE teachers SET last_status='%s', num_weekday=num_weekday+1 WHERE name='%s'" % (time, teacher)
            if time == 'weekday_night':
                sql = "UPDATE teachers SET last_status='%s', num_weekday_night=num_weekday_night+1 WHERE name='%s'" % (time, teacher)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                # print("修改成功")
            except:
                # 发生错误时回滚
                db.rollback()
                # print("修改失败")
        self.name_list = self.name_list.drop(_df.index)
        print(f'分配完{time}后剩余人员数量：', len(self.name_list))

    def variance(self):
        # 读取数据库一列数据
        sql = "SELECT num_weekday,num_weekday_night, num_weekend, num_weekend_night FROM teachers"
        cursor.execute(sql)
        datalist = []
        alldata = cursor.fetchall()

        for j in range(4):
            for i in alldata:
                datalist.append(i[j])
            variance = np.std(datalist)
            print(f'{"weekday" if j==0 or j==1 else "weekend"}{"_night" if j==1 or 3 else ""}的标准差为：', variance)


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

        # filedata.save(f_path)
        # print(result)
        return result







