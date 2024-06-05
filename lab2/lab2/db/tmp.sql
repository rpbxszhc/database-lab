insert into app_sl(id, grade, lesson_id, stu_id, is_retaking) values
(11, 80, 4, 2222222222, 1);
update app_stu set retake_chances = 3 where id = '5555555555';

select * from grade_info where id = 4444444444 and grade is not null and is_retaking = 0;