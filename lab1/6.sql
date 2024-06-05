DROP TRIGGER IF EXISTS book_reserved_trigger;

DELIMITER //
CREATE TRIGGER book_reserved_trigger
AFTER INSERT ON reserve
FOR EACH ROW
BEGIN
    UPDATE Book 
    SET bstatus = 2, reserve_Times = reserve_Times + 1
    WHERE bid = NEW.book_ID;
END;
//
DELIMITER ;


DROP TRIGGER IF EXISTS reservation_change_trigger;

DELIMITER //
CREATE TRIGGER reservation_change_trigger
AFTER DELETE ON reserve
FOR EACH ROW
BEGIN
    UPDATE Book 
    SET reserve_Times = reserve_Times - 1
    WHERE bid = OLD.book_ID;
END;
//
DELIMITER ;


DROP TRIGGER IF EXISTS cancel_reservation_trigger;

DELIMITER //
CREATE TRIGGER cancel_reservation_trigger
AFTER DELETE ON reserve
FOR EACH ROW
BEGIN
    DECLARE reserve_count INT;
    DECLARE b_status INT;
    SELECT reserve_Times INTO reserve_count FROM Book WHERE bid = OLD.book_ID;
    SELECT bstatus INTO b_status FROM Book WHERE bid = OLD.book_ID;
    IF reserve_count = 0 and b_status = 2 THEN
        UPDATE Book 
        SET bstatus = 0
        WHERE bid = OLD.book_ID;
    END IF;
END;
//
DELIMITER ;

INSERT INTO reserve (Reader_ID, book_ID, reserve_Date) VALUES ('R001', 'B012', '2024-05-9');
SELECT * FROM Book WHERE bid = 'B012';


DELETE FROM reserve WHERE Reader_ID = 'R001' AND book_ID = 'B012';
SELECT * FROM Book WHERE bid = 'B012';
