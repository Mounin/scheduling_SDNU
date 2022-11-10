from extension import db
import pandas as pd

# 读入文件并转化为列表
f_path = 'data/pre1104/origin.xlsx'
teacher_list = pd.read_excel(f_path)
teacher_list.replace('\s+', '', regex=True, inplace=True)  # 忽略空格
teacher_list = teacher_list.values


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    last_status = db.Column(db.String(255))
    num_weekday = db.Column(db.Integer)
    num_weekday_night = db.Column(db.Integer)
    num_weekend = db.Column(db.Integer)
    num_weekend_night = db.Column(db.Integer)
    cq = db.Column(db.Boolean)
    qfs = db.Column(db.Boolean)

    @staticmethod
    def init_db():
        for ret in teacher_list:
            teacher = Teacher()
            # teacher.id = ret[0]
            teacher.name = ret[0]
            teacher.last_status = ret[1]
            teacher.num_weekday = ret[2]
            teacher.num_weekday_night = ret[3]
            teacher.num_weekend = ret[4]
            teacher.num_weekend_night = ret[5]
            teacher.cq = ret[6]
            teacher.qfs = ret[7]
            db.session.add(teacher)
        db.session.commit()