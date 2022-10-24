weekday: 工作日白天<br>
weekday_night: 工作日晚上<br>
weekend: 休息日白天<br>
weekend_night: 休息日晚上<br>

num_weekday: 工作日白天人数<br>
num_weekday_night: 工作日晚上人数<br>
num_weekend: 休息日白天人数<br>
num_weekend_night: 休息日晚上人数<br>

### version1.0
分配顺序：休息日晚上 -> 休息日白天 -> 工作日白天 -> 工作日晚上 <br>
如果上次安排在休息日晚上或者休息日白天，则本次不会再安排在休息日的任何一个时间<br>
工作日白天和工作日晚上随机分配<br>
记录本次分配的时间段以便于下次分配<br>
分配校区<br>

输入：人员列表（excel）、长清湖校区四个班次的人数、千佛山校区四个班次的人数<br>
输入列表之前先将条件（是否必须在某个校区）修改到数据库<br>

