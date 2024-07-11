create database mydatabase;

use mydatabase;

create table student(
	id int primary key,
    name varchar(50),
    marks int
);

insert into student values
    (7001, 'Bronnie', 192),
    (7002, 'Lemmie', 138),
    (7003, 'Danya', 211),
    (7004, 'Denna', 183),
    (7005, 'Jocelin', 73),
    (7006, 'Malissa', 310),
    (7007, 'Ichabod', 226),
    (7008, 'Beverlie', 197),
    (7009, 'Corrine', 126),
    (7010, 'Tate', 124)
;

alter table student modify name varchar(50) not null;

alter table student add result varchar(20);

update student
set result = case
	when marks >= 150 then 'pass'
    else 'fail'
end;
	
-- delete from student where result = 'fail';

-- drop table student;

-- drop database mydatabase; 