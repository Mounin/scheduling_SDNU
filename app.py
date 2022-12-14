import os
import time
import pandas as pd

from flask import Flask, request,  Response
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from extension import db, cors
from model import Teacher
from src.schedule_start import schedule_start
from src.sql import sql_select_all, sql_select
from src.teacherOperation import update_teacher, delete_teacher, update_teacher_database, check_database

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teachers.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# 获取上传文件
@app.route("/upload/", methods=['POST'])
def do_upload():
    """处理上传文件"""
    filedata = request.files['fileTest']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    #######################################
    # 毫秒级时间戳
    file_name = str(round(time.time() * 1000))
    dir = str(time.strftime('%y%m%d', time.localtime()))
    upload_path = os.path.join(basepath, 'uploads/' + dir)
    # 判断文件夹是否存在
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    #######################################
    file_path = str(file_name) + str(filedata.filename)
    f_path = upload_path + '/' + file_path
    filedata.save(f_path)
    f_path = {'f_path': f_path}
    check_database(f_path)
    return f_path


# 获取每个值班时间段的人数
@app.route('/number', methods=['POST'])
def number():
    form = request.form
    shifts = {'qfs_num_weekday': form.get('qfs_num_weekday'),
              'qfs_num_weekday_night': form.get('qfs_num_weekday_night'),
              'qfs_num_weekend': form.get('qfs_num_weekend'),
              'qfs_num_weekend_night': form.get('qfs_num_weekend_night'),
              'cq_num_weekday': form.get('cq_num_weekday'),
              'cq_num_weekday_night': form.get('cq_num_weekday_night'),
              'cq_num_weekend': form.get('cq_num_weekend'),
              'cq_num_weekend_night': form.get('cq_num_weekend_night')}
    return shifts


# 开始排班
@app.route('/submit', methods=['POST'])
def submit():
    form = request.form
    params = {'f_path': form.get('f_path'),
              'qfs_num_weekday': form.get('qfs_num_weekday'),
              'qfs_num_weekday_night': form.get('qfs_num_weekday_night'),
              'qfs_num_weekend': form.get('qfs_num_weekend'),
              'qfs_num_weekend_night': form.get('qfs_num_weekend_night'),
              'cq_num_weekday': form.get('cq_num_weekday'),
              'cq_num_weekday_night': form.get('cq_num_weekday_night'),
              'cq_num_weekend': form.get('cq_num_weekend'),
              'cq_num_weekend_night': form.get('cq_num_weekend_night')}
    schedule_start(params)
    result_paths = schedule_start(params)
    cq_file = pd.read_excel(result_paths[0], index_col=0)
    qfs_file = pd.read_excel(result_paths[1], index_col=0)
    result = pd.concat([cq_file, qfs_file], keys=['长清湖校区', '千佛山校区'])
    writer = pd.ExcelWriter('山东师范大学核酸检测排班.xlsx')
    result.to_excel(writer)
    writer.save()
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    f_path = basepath + '/山东师范大学核酸检测排班.xlsx'
    with open(f_path, 'rb') as f:
        stream = f.read()
    response = Response(stream, content_type='application/octet-stream')
    response.headers['Content-disposition'] = 'attachment; filename=test.xlsx'
    return response


# 提交修改
@app.route('/edit', methods=['POST'])
def edit():
    form = request.form
    teacherDetail = {
        'id': form.get('id'),
        'name': form.get('name'),
        'last_status': form.get('last_status'),
        'num_weekday': form.get('num_weekday'),
        'num_weekday_night': form.get('num_weekday_night'),
        'num_weekend': form.get('num_weekend'),
        'num_weekend_night': form.get('num_weekend_night'),
        'cq': form.get('cq'),
        'qfs': form.get('qfs')
    }
    update_teacher(teacherDetail)
    return teacherDetail


# 删除老师
@app.route('/delete', methods=['POST'])
def delete():
    teacher_id = request.form.get('id')
    delete_teacher(teacher_id)
    return teacher_id


# 更新数据库
@app.route('/update_database', methods=['POST'])
def update_database():
    """处理上传文件"""
    filedata = request.files['fileTest']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    #######################################
    # 毫秒级时间戳
    file_name = str(round(time.time() * 1000))
    dir = str(time.strftime('%y%m%d', time.localtime()))
    upload_path = os.path.join(basepath, 'update/' + dir)
    # 判断文件夹是否存在
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    #######################################
    file_path = str(file_name) + str(filedata.filename)
    f_path = upload_path + '/' + file_path
    filedata.save(f_path)
    f_path = {'f_path': f_path}
    update_teacher_database(f_path)
    return f_path


# 查询teachers表
@app.route('/teachers/', methods=['GET'])
def get_all_teachers():
    select_sql = f"SELECT * FROM teachers"
    teacher_list = sql_select_all(select_sql)
    results = [
                {
                    'id': teacher[0],
                    'name': teacher[1],
                    'last_status': teacher[2],
                    'num_weekday': teacher[3],
                    'num_weekday_night': teacher[4],
                    'num_weekend': teacher[5],
                    'num_weekend_night': teacher[6],
                    'cq': teacher[7],
                    'qfs': teacher[8],
                } for teacher in teacher_list
            ]
    print(results)
    return {
        'status': 'success',
        'message': '数据查询成功',
        'results': results
    }


# 根据teacher_id查询teacher信息
@app.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher_by_id(teacher_id):
    select_sql = f"SELECT * FROM teachers WHERE id={teacher_id}"
    teacher = sql_select(select_sql)
    return f"{teacher}"
    

@app.cli.command()  # 自定义指令
def create():
    db.drop_all()
    db.create_all()
    Teacher.init_db()


# class TeacherAPI(MethodView):
#     def get(self, teacher_id):
#         if not teacher_id:
#             teachers: [Teacher] = Teacher.query.all()
#             results = [
#                 {
#                     'id': teacher.id,
#                     'name': teacher.name,
#                     'last_status': teacher.last_status,
#                     'num_weekday': teacher.num_weekday,
#                     'num_weekday_night': teacher.num_weekday_night,
#                     'num_weekend': teacher.num_weekend,
#                     'num_weekend_night': teacher.num_weekend_night,
#                     'cq': teacher.cq,
#                     'qfs': teacher.qfs,
#                 } for teacher in teachers
#             ]
#             return {
#                 'status': 'success',
#                 'message': '数据查询成功',
#                 'results': results
#             }
#         teacher: Teacher = Teacher.query.get(teacher_id)
#         return {
#             'status': 'success',
#             'message': '数据查询成功',
#             'result': {
#                 'id': teacher.id,
#                 'name': teacher.name,
#                 'last_status': teacher.last_status,
#                 'num_weekday': teacher.num_weekday,
#                 'num_weekday_night': teacher.num_weekday_night,
#                 'num_weekend': teacher.num_weekend,
#                 'num_weekend_night': teacher.num_weekend_night,
#                 'cq': teacher.cq,
#                 'qfs': teacher.qfs,
#             }
#         }
#
#     def put(seLf, teacher_id):
#         teacher: Teacher = Teacher.query.get(teacher_id)
#         teacher.name = request.json.get('name')
#         teacher.last_status = request.json.get('last_status')
#         teacher.num_weekday = request.json.get('num_weekday')
#         teacher.num_weekday_night = request.json.get('num_weekday_night')
#         teacher.num_weekend = request.json.get('num_weekend')
#         teacher.num_weekend_night = request.json.get('num_weekend_night')
#         teacher.cq = request.json.get('cq')
#         teacher.qfs = request.json.get('qfs')
#         db.session.commit()
#         return {
#             'status': 'success',
#             'message': '数据修改成功',
#         }
#
#     def delete(self, teacher_id):
#         teacher = Teacher.query.get(teacher_id)
#         db.session.delete(teacher)
#         db.session.commit()
#         return {
#             'status': 'success',
#             'message': '数据删除成功',
#         }
#
#     def post(self):
#         form = request.json
#         teacher = Teacher()
#         teacher.name = form.get('name')
#         teacher.last_status = form.get('last_status')
#         teacher.num_weekday = form.get('num_weekday')
#         teacher.num_weekday_night = form.get('num_weekday_night')
#         teacher.num_weekend = form.get('num_weekend')
#         teacher.num_weekend_night = form.get('num_weekend_night')
#         teacher.cq = form.get('cq')
#         teacher.qfs = form.get('qfs')
#         db.session.add(teacher)
#         db.session.commit()
#         return {
#             'status': 'success',
#             'message': '数据添加成功',
#         }
#
# teacher_view = TeacherAPI.as_view('teacher_api')
# app.add_url_rule('/teachers/', defaults={'teacher_id': None}, view_func=teacher_view, methods=['GET', ])
# app.add_url_rule('/teachers/', view_func=teacher_view, methods=['POST', ])
# app.add_url_rule('/teachers/<int:teacher_id>', view_func=teacher_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
