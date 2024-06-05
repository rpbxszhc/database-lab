drop view if exists stu_info;
create view stu_info as
	(select app_stu.id, password, img, sname as name, gender, prize, punishment, status, retake_chances, birthday, 
	data_in, mname as major, dname as department, compute_gpa(app_stu.id) as avg_gpa
    from app_stu, app_major, app_department
    where major_id = app_major.id and department_id = app_department.id order by app_stu.id);

select * from stu_info;

drop view if exists grade_info;
create view grade_info as
	(select sname, app_stu.id as id, app_lesson.id as lid, lname, grade, is_retaking
    from app_lesson, app_sl, app_stu
    where app_lesson.id = app_sl.lesson_id and app_stu.id = app_sl.stu_id);
    
select * from grade_info;

drop view if exists les_info;
create view les_info as
	(select app_lesson.id as id, lname, teacher, credit, hour, mname, dname
    from app_department, app_lesson, app_major
    where app_department.id = app_major.department_id and app_lesson.major_id = app_major.id);
    
select * from les_info;

drop view if exists sl_info;
create view sl_info as
	(select app_sl.id as id, app_stu.id as sid, app_stu.sname as sname, app_lesson.id as lid, app_lesson.lname as lname,
    teacher, credit, hour, is_retaking, grade from app_stu, app_lesson, app_sl
    where app_stu.id = app_sl.stu_id and app_sl.lesson_id = app_lesson.id);
    
select * from sl_info;
