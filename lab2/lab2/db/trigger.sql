DROP TRIGGER IF EXISTS sl_delete;

DELIMITER //
CREATE TRIGGER sl_delete
AFTER INSERT ON app_sl
FOR EACH ROW
BEGIN
    declare fail_cnt int default 0;
    select count(*) into fail_cnt from app_sl where stu_id = new.stu_id and grade < 60;
    if fail_cnt >= 3 then
		update app_stu set status = 1 where id = new.stu_id;
	else
		update app_stu set status = 0 where id = new.stu_id;
	end if;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS sl_update;

DELIMITER //
CREATE TRIGGER sl_update
AFTER update ON app_sl
FOR EACH ROW
BEGIN
    declare fail_cnt int default 0;
    select count(*) into fail_cnt from app_sl where stu_id = new.stu_id and grade < 60;
    if fail_cnt >= 3 then
		update app_stu set status = 1 where id = new.stu_id;
	else
		update app_stu set status = 0 where id = new.stu_id;
	end if;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS sl_delete;

DELIMITER //
CREATE TRIGGER sl_delete
AFTER delete ON app_sl
FOR EACH ROW
BEGIN
    declare fail_cnt int default 0;
    select count(*) into fail_cnt from app_sl where stu_id = old.stu_id and grade < 60;
    if fail_cnt >= 3 then
		update app_stu set status = 1 where id = old.stu_id;
	else
		update app_stu set status = 0 where id = old.stu_id;
	end if;
END;
//
DELIMITER ;