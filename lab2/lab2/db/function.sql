DELIMITER //

DROP FUNCTION IF EXISTS compute_gpa//
CREATE FUNCTION compute_gpa(
    id VARCHAR(10)
)
RETURNS FLOAT
READS SQL DATA
BEGIN
    DECLARE avg_grade FLOAT;
    SELECT AVG(grade) INTO avg_grade FROM app_sl WHERE stu_id = id and grade is not null;

    IF avg_grade >= 95 THEN
		RETURN 4.3;
	ELSEIF avg_grade >= 90 THEN
		RETURN 4.0;
	ELSEIF avg_grade >= 85 THEN
		RETURN 3.7;
	ELSEIF avg_grade >= 82 THEN
		RETURN 3.3;
	ELSEIF avg_grade >= 78 THEN
		RETURN 3.0;
	ELSEIF avg_grade >= 75 THEN
		RETURN 2.7;
    ELSEIF avg_grade >= 72 THEN
		RETURN 2.3;   
	ELSEIF avg_grade >= 68 THEN
		RETURN 2.0;
	ELSEIF avg_grade >= 65 THEN
		RETURN 1.7;
	ELSEIF avg_grade >= 62 THEN
		RETURN 1.3;
	ELSEIF avg_grade >= 60 THEN
		RETURN 1.0;
	ELSE 
		RETURN 0;
	END IF;
END //

DELIMITER ;


