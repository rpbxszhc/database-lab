DELIMITER //
DROP procedure IF EXISTS retake//
CREATE procedure retake(
    in sid varchar(10),
    in lid varchar(10),
    in is_quit bool,
    in new_grade smallint
)
BEGIN
	declare old_grade, cnt, chances, isretaking, retaking_cnt int default 0;
    select grade, count(*), is_retaking into old_grade, cnt, isretaking from app_sl 
    where sid = stu_id and lid = lesson_id group by grade, is_retaking;
    
    select count(*) into retaking_cnt from app_sl where sid = stu_id and is_retaking = 1;
    
    select retake_chances into chances from app_stu where sid = id;
    start transaction;
    if cnt > 0 then
		if is_quit then
			delete from app_sl where sid = stu_id and lid = lesson_id;
		elseif new_grade > old_grade and isretaking = 1 then
			update app_sl set grade = new_grade, is_retaking = 0 where sid = stu_id and lid = lesson_id;
		elseif new_grade > old_grade then
			update app_sl set grade = new_grade where sid = stu_id and lid = lesson_id;
		end if;
	end if;
	if ((chances > retaking_cnt) or (chances = retaking_cnt and isretaking))  and cnt > 0 then
		update app_stu set retake_chances = retake_chances - 1 where sid = id;
        set @state = 0;
        commit;
	else
		set @state = -1000;
        rollback;
	end if;
END //
DELIMITER ;

select * from app_sl;
select * from app_stu;
select * from app_sl where is_retaking = 1;
call retake(2222222222, 6, 1, 90);

select @state;

DELIMITER //
DROP procedure IF EXISTS edit_stu_id//
CREATE procedure edit_stu_id(
    in old_id varchar(10),
    in new_id varchar(10)
)
BEGIN
	start transaction;
	SET FOREIGN_KEY_CHECKS = 0;
    update app_stu set id = new_id where id = old_id;
    update app_sl set stu_id = new_id where stu_id = old_id;
    SET FOREIGN_KEY_CHECKS = 1;
    set @state = 0;
    commit;
END //
DELIMITER ;

call edit_stu_id(3333333333,4444444444);
select * from app_stu;
select * from app_sl;

DELIMITER //
DROP procedure IF EXISTS edit_les_id//
CREATE procedure edit_les_id(
    in old_id varchar(10),
    in new_id varchar(10)
)
BEGIN
	start transaction;
	SET FOREIGN_KEY_CHECKS = 0;
    update app_lesson set id = new_id where id = old_id;
    update app_sl set lesson_id = new_id where lesson_id = old_id;
    SET FOREIGN_KEY_CHECKS = 1;
    set @state = 0;
    commit;
END //
DELIMITER ;

DELIMITER //
DROP procedure IF EXISTS edit_major_id//
CREATE procedure edit_major_id(
    in old_id varchar(3),
    in new_id varchar(3)
)
BEGIN
DECLARE done INT DEFAULT 0;
	start transaction;
	SET FOREIGN_KEY_CHECKS = 0;
	update app_stu set major_id = new_id where major_id = old_id;
    update app_lesson set major_id = new_id where major_id = old_id;
    update app_major set id = new_id where id = old_id;
    SET FOREIGN_KEY_CHECKS = 1;
    set @state = 0;
    commit;
END //
DELIMITER ;

call edit_major_id(6, 2);


DELIMITER //
DROP procedure IF EXISTS edit_dep_id//
CREATE procedure edit_dep_id(
    in old_id varchar(3),
    in new_id varchar(3)
)
BEGIN
	start transaction;
	SET FOREIGN_KEY_CHECKS = 0;
    update app_department set id = new_id where id = old_id;
    update app_major set department_id = new_id where department_id = old_id;
    SET FOREIGN_KEY_CHECKS = 1;
    set @state = 0;
    commit;
END //
DELIMITER ;