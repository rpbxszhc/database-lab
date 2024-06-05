DELIMITER //
DROP PROCEDURE IF EXISTS updateReaderID;
CREATE PROCEDURE updateReaderID(
    IN old_reader_id CHAR(8),
    IN new_reader_id CHAR(8)
)
BEGIN
    DECLARE reader_count INT;
    
    -- 检查旧的读者ID是否存在
    SELECT COUNT(*) INTO reader_count FROM Reader WHERE rid = old_reader_id;
    
    -- 如果旧的读者ID存在，则执行更新操作
    IF reader_count > 0 THEN
		SET Foreign_key_checks=0; #关闭外键约束检查
        UPDATE Reader SET rid = new_reader_id WHERE rid = old_reader_id;
        UPDATE Borrow SET reader_ID = new_reader_id WHERE reader_ID = old_reader_id;
        UPDATE Reserve SET reader_ID = new_reader_id WHERE reader_ID = old_reader_id;
        SET Foreign_key_checks=1; #开启外键约束检查
        SELECT CONCAT('读者ID ', old_reader_id, ' 已成功修改为 ', new_reader_id, '。');
    ELSE
        SELECT CONCAT('error:读者ID ', old_reader_id, ' 不存在。');
    END IF;
    
END //

DELIMITER ;

CALL updateReaderID('R006', 'R999');

SELECT * FROM Reader;

SELECT * FROM Borrow;

SELECT * FROM Reserve;