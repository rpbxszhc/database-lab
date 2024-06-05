# 1
select	b.bid, b.bname, Borrow.borrow_Date
from	Book B,Reader R,Borrow
where	R.rid=Borrow.reader_ID and Borrow.book_ID=b.bid and R.rname='Rose';

# 2
SELECT rid, rname
FROM Reader
WHERE rid NOT IN (SELECT reader_ID FROM Borrow)
	and rid NOT IN (SELECT reader_ID FROM Reserve);


# 3.1

SELECT b.author, COUNT(*) AS borrow_count
FROM Borrow bo, Book b
WHERE bo.book_ID = b.bid
GROUP BY b.author
ORDER BY borrow_count DESC
LIMIT 1;

# 3.2

SELECT author, SUM(borrow_Times) AS total_borrows
FROM Book
GROUP BY author
ORDER BY total_borrows DESC
LIMIT 1;

# 4

SELECT b.bid, b.bname
FROM Borrow bo, Book b
WHERE bo.book_ID = b.bid
AND bo.return_Date IS NULL
AND b.bname LIKE '%MySQL%';

# 5

SELECT r.rname
FROM Reader r, Borrow bo
WHERE r.rid = bo.reader_ID
GROUP BY r.rid
HAVING COUNT(*) > 3;

# 6

SELECT r.rid, r.rname
FROM Reader r
WHERE r.rid NOT IN (
    SELECT bo.reader_ID
    FROM Borrow bo, Book b
    WHERE bo.book_ID = b.bid
    AND b.author = 'J.K. Rowling'
);

# 7

SELECT r.rid, r.rname, COUNT(*) AS borrow_count
FROM Borrow bo, Reader r
WHERE bo.reader_ID = r.rid
AND YEAR(bo.borrow_Date) = 2024
GROUP BY r.rid, r.rname
ORDER BY borrow_count DESC
LIMIT 3;

# 8

DROP view IF EXISTS Message;
create view Message as
	(select	rid, rname, bid, bname, Borrow_date
	from	Reader r, Book b, Borrow
	where	rid = reader_ID and  book_ID = bid);
						
select	rid, count(distinct bid) as Book_num
from	Message
where	year(borrow_date) = 2024
group by 	rid;
