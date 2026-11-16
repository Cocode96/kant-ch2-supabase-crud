create temporary table kant_ch2_tx_2337 (id int primary key, stock int not null check (stock >= 0));
insert into kant_ch2_tx_2337 values (1,10);
create temporary table kant_ch2_tx_results_2337 (step text, observed text, expected text);
insert into kant_ch2_tx_results_2337 select 'initial stock',stock::text,'10' from kant_ch2_tx_2337;
begin;
update kant_ch2_tx_2337 set stock=8 where id=1;
commit;
begin;
insert into kant_ch2_tx_results_2337 select 'COMMIT persisted',stock::text,'8' from kant_ch2_tx_2337;
commit;
begin;
update kant_ch2_tx_2337 set stock=5 where id=1;
rollback;
insert into kant_ch2_tx_results_2337 select 'ROLLBACK restored',stock::text,'8' from kant_ch2_tx_2337;
do $$
begin
  begin
    update kant_ch2_tx_2337 set stock=5 where id=1;
    update kant_ch2_tx_2337 set stock=-1 where id=1;
  exception when check_violation then
    insert into kant_ch2_tx_results_2337 values ('CHECK SQLSTATE',SQLSTATE,'23514');
    insert into kant_ch2_tx_results_2337 select 'exception block rollback',stock::text,'8' from kant_ch2_tx_2337;
  end;
end $$;
select step, observed, expected, observed=expected as passed from kant_ch2_tx_results_2337;