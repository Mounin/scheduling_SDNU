import pandas as pd
from extension import db


class NewTeacher(db.Model):
    __tablename__ = 'newTeacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    cq = db.Column(db.Boolean)
    qfs = db.Column(db.Boolean)

    @staticmethod
    def init_db(f_path):
        teacher_list = pd.read_excel(f_path)
        teacher_list.replace('\s+', '', regex=True, inplace=True)  # 忽略空格

        teacher_list = teacher_list.values
        for ret in teacher_list:
            teacher = NewTeacher()
            teacher.name = ret[0]
            teacher.cq = ret[1]
            teacher.qfs = ret[2]
            db.session.add(teacher)
        db.session.commit()


class ShiftNum(db.Model):
    __tablename__ = 'shift_num'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    time = db.Column(db.String(255))
    num = db.Column(db.String(255))

    @staticmethod
    def init_db(shifts):
        for shift in shifts:
            (key, value), = shift.items()
            shift = ShiftNum()
            shift.time = key
            shift.num = value
            db.session.add(shift)
        db.session.commit()