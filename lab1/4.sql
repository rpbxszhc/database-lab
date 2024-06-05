DROP PROCEDURE IF EXISTS borrowBook;

DELIMITER //

CREATE PROCEDURE borrowBook(
    IN r_id CHAR(8),
    IN b_id CHAR(8),
    IN bdate DATE
)
borrow_book:BEGIN
    DECLARE borrow_count INT;
    DECLARE already_borrowed INT;
    DECLARE reserve_count INT;
    
    -- 检查读者已借阅的书籍数量
    SELECT COUNT(*) INTO borrow_count FROM Borrow 
    WHERE reader_ID = r_id AND return_Date IS NULL;
    
    -- 检查是否已经借阅了三本书
    IF borrow_count >= 3 THEN
        SELECT '借阅失败：该读者已经借阅了三本书且未归还。';
        LEAVE borrow_book;
    END IF;
    
    -- 检查是否已经借阅了相同的书籍
    SELECT COUNT(*) INTO already_borrowed FROM Borrow 
    WHERE reader_ID = r_id AND book_ID = b_id AND borrow_Date = bdate;
    
    IF already_borrowed > 0 THEN
        SELECT '借阅失败：同一天不允许同一个读者重复借阅同一本书。';
        LEAVE borrow_book;
    END IF;
    
    -- 检查是否有人预约了该图书
    SELECT reserve_Times INTO reserve_count FROM Book WHERE bid = b_id;
    
    IF reserve_count > 0 THEN
        -- 检查当前借阅者是否有预约
        SELECT COUNT(*) INTO reserve_count FROM Reserve 
        WHERE reader_ID = r_id AND book_ID = b_id;
        
        IF reserve_count = 0 THEN
            SELECT '借阅失败：该图书存在预约记录，当前借阅者没有预约。';
            LEAVE borrow_book;
        END IF;
        
        UPDATE Book SET reserve_Times = reserve_Times - 1 WHERE bid = b_id;
        
        -- 删除借阅者对该图书的预约记录
        DELETE FROM Reserve WHERE reader_ID = r_id AND book_ID = b_id;
    END IF;
    
    -- 更新图书表中的 borrow_times 和 bstatus 属性
    UPDATE Book SET borrow_Times = borrow_Times + 1, bstatus = 1 WHERE bid = b_id;
    
    -- 插入借阅信息到借阅表
    SET Foreign_key_checks=0; #关闭外键约束检查
    INSERT INTO Borrow (reader_ID, book_ID, borrow_date, return_Date)
    VALUES (r_id, b_id, bdate, null);
    SET Foreign_key_checks=1; #开启外键约束检查
    
    SELECT '借阅成功。';
    
    -- 结束存储过程
    LEAVE borrow_book;
    
    -- 标签，用于退出存储过程
END //
    
DELIMITER ;

SELECT * FROM Borrow;

CALL borrowBook('R001', 'B008', '2024-05-9');

CALL borrowBook('R001', 'B001', '2024-05-9');
SELECT * FROM Reserve;
SELECT * FROM Book WHERE bid = 'B001';

CALL borrowBook('R001', 'B001', '2024-05-9');

CALL borrowBook('R005', 'B008', '2024-05-9');
