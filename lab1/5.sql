DROP PROCEDURE IF EXISTS returnBook;

DELIMITER //

CREATE PROCEDURE returnBook(
    IN r_id CHAR(8),
    IN b_id CHAR(8),
    IN rdate DATE
)
return_book:BEGIN
    DECLARE flag INT;
    
    -- 检查该读者是否借阅了这本书
    SELECT count(*) INTO flag FROM Borrow 
    WHERE book_ID = b_id and Reader_ID = r_id and return_date IS NULL;
    
    IF flag = 0 THEN
        SELECT '还书失败：您未借阅该图书。';
        LEAVE return_book;
    END IF;
    
    -- 更新借阅表中的还书日期
    UPDATE Borrow SET return_date = rdate 
    WHERE reader_ID = r_id AND book_ID = b_id AND return_date IS NULL;
    
    -- 更新图书表中的 bstatus 属性
    SELECT reserve_Times INTO flag FROM Book WHERE bid = b_id;
    IF flag = 0 THEN
		UPDATE Book SET bstatus = 0 WHERE bid = b_id;
	ELSE
		UPDATE Book SET bstatus = 2 WHERE bid = b_id;
	END IF;
    SELECT '还书成功。';
    
    -- 结束存储过程
    LEAVE return_book;
    
    -- 标签，用于退出存储过程
END //

DELIMITER ;


CALL returnBook('R001', 'B008', '2024-05-10');

CALL returnBook('R001', 'B001', '2024-05-10');

SELECT * FROM Book WHERE bid = 'B001';
SELECT * FROM Borrow WHERE book_ID = 'B001' and reader_ID = 'R001'