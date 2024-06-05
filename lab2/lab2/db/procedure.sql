DELIMITER //
DROP procedure IF EXISTS delete_stu//
CREATE procedure delete_stu(
    in sid varchar(10)
)
BEGIN
    delete from app_sl where stu_id = sid;
    delete from app_stu where id = sid;
END //
DELIMITER ;

DELIMITER //
DROP procedure IF EXISTS delete_les//
CREATE procedure delete_les(
    in lid varchar(10)
)
BEGIN
    delete from app_sl where lesson_id = lid;
    delete from app_lesson where id = lid;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS delete_major//
CREATE PROCEDURE delete_major(
    IN mid VARCHAR(10)
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE student_id VARCHAR(10);
    DECLARE lesson_id VARCHAR(10);
    
    -- 声明一个游标，用于获取特定 major_id 的学生 id
    DECLARE cur_stu CURSOR FOR
        SELECT id FROM app_stu WHERE major_id = mid;
        
    -- 声明一个游标，用于获取特定 major_id 的课程 id
    DECLARE cur_les CURSOR FOR
        SELECT id FROM app_lesson WHERE major_id = mid;
    
    -- 定义一个继续处理游标的条件
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur_stu;
    read_student_loop: LOOP
        FETCH cur_stu INTO student_id;
        IF done THEN
            LEAVE read_student_loop; -- 如果学生游标没有更多数据，则跳出循环
        END IF;
        CALL delete_stu(student_id); -- 调用删除学生记录的存储过程
    END LOOP;
    
    CLOSE cur_stu; -- 关闭学生游标

    -- 重置 done 变量，用于处理课程游标
    SET done = 0;

    OPEN cur_les;
    read_lesson_loop: LOOP
        FETCH cur_les INTO lesson_id;
        IF done THEN
            LEAVE read_lesson_loop; -- 如果课程游标没有更多数据，则跳出循环
        END IF;
        CALL delete_les(lesson_id); -- 调用删除课程记录的存储过程
    END LOOP;

    CLOSE cur_les; -- 关闭课程游标
    delete from app_major where id = mid;
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS delete_dep//
CREATE PROCEDURE delete_dep(
    IN did VARCHAR(10)
)
begin
	DECLARE done INT DEFAULT 0;
    DECLARE major_id VARCHAR(10);
    DECLARE cur_major CURSOR FOR
        SELECT id FROM app_major WHERE department_id = did;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN cur_major;
    read_loop: LOOP
        FETCH cur_major INTO major_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        CALL delete_major(major_id);
    END LOOP;
    CLOSE cur_major; -- 关闭课程游标
    delete from app_department where id = did;
end//
DELIMITER ;