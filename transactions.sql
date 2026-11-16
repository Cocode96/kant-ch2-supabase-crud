-- psql �Ǵ� SQL �������� ���� ���ǿ��� ���Ϻ��� ����.
-- TEMP ���̺��� ����ϹǷ� ��/�Ǽ��� �����Ϳ� �������̴�.
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

-- �Ʒ� BEGIN ~ ���� UPDATE���� �����ϸ� CHECK ������ �߻��ؾ� �Ѵ�.
begin;
update transaction_demo set stock = 5 where id = 1;
select 'inside transaction: 5' as step, * from transaction_demo;
update transaction_demo set stock = -1 where id = 1; -- �ǵ��� ����

-- ���� �� ���� ���ǿ��� ������ ����. �� 5�� �ٲ� �۾��� �Բ� ��ҵȴ�.
rollback;
select 'after rollback: 8' as step, * from transaction_demo;
drop table transaction_demo;

