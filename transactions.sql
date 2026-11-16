-- psql 또는 SQL 편집기의 같은 세션에서 블록별로 실행.
-- TEMP 테이블만 사용하므로 팀/실서비스 데이터와 독립적이다.
create temporary table transaction_demo (
    id integer primary key,
    stock integer not null check (stock >= 0)
);
insert into transaction_demo values (1, 10);
select 'before commit' as step, * from transaction_demo;
begin;
update transaction_demo set stock = 8 where id = 1;
commit;
select 'after commit: 8' as step, * from transaction_demo;

-- 아래 BEGIN ~ 실패 UPDATE까지 실행하면 CHECK 위반이 발생해야 한다.
begin;
update transaction_demo set stock = 5 where id = 1;
select 'inside transaction: 5' as step, * from transaction_demo;
update transaction_demo set stock = -1 where id = 1; -- 의도적 실패

-- 실패 후 같은 세션에서 별도로 실행. 위 5로 바꾼 작업도 함께 취소된다.
rollback;
select 'after rollback: 8' as step, * from transaction_demo;
drop table transaction_demo;

