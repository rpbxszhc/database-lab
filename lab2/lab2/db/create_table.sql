drop table if exists SC;
drop table if exists Stu;

create table Stu(
	sno char(8) primary key,
	sname varchar(100) not null,
	gender char(1),
    major varchar(100),
    prize varchar(100) default null,
    punishment varchar(100) default null,
    state int default 0,
    fail_cnt int default 0,
    birthday date,
    date_in date,
    CONSTRAINT check_birthday CHECK (birthday < date_in),
    CONSTRAINT check_gender CHECK (gender in ("f", "m"))
);

drop table if exists Cls;

create table Cls(
	cno char(8) primary key,
    cname varchar(100) not null,
    tname varchar(100) default null,
    semester varchar(50),
    department varchar(100),
    credit float not null,
    hours int not null,
    constraint check_credit check (credit > 0.0),
    constraint check_hours check (hours > 0)
);

create table SC(
	sno char(8),
    cno char(8),
	foreign key(sno) references Stu(sno),
    foreign key(cno) references Cls(cno),
    primary key(sno, cno),
    grade int default null,
    constraint check_scgrade check (grade >= 0 and grade <= 100)
);