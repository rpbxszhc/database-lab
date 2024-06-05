Create table Book(
	bid char(8) Primary Key,
	bname varchar(100) NOT NULL,
	author varchar(50),
	price float,
	bstatus int Default 0,
    borrow_Times int Default 0,
    reserve_Times int Default 0);
    
Create table Reader(
	rid char(8) Primary Key,
	rname varchar(20),
	age int,
	address varchar(100));
    
Create table Borrow(
	book_ID char(8),
	reader_ID char(8),
	borrow_Date date,
	return_Date date,
	Primary Key(book_ID, reader_ID, borrow_Date),
	Foreign Key(book_ID) references Book(bid),
	Foreign Key(Reader_ID) references Reader(rid));
    
Create table Reserve(
	book_ID char(8),
	reader_ID char(8),
	reserve_Date date default (curdate()),
	take_Date date,
	Primary Key(book_ID, reader_ID, reserve_Date),
	Foreign Key(book_ID) references Book(bid),
	Foreign Key(Reader_ID) references Reader(rid),
    CONSTRAINT chk_take_Date CHECK (take_Date > reserve_Date));