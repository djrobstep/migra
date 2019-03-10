create table table1 (
  id serial primary key
);
create table table2 (
  id serial primary key,
  t text
);

create function trigger_func() returns trigger language plpgsql volatile as $$
begin
  RAISE NOTICE 'Hello';
end;
$$;

create trigger trigger_name after insert on table1 for each row
  execute procedure trigger_func();

create trigger trigger_name after insert on table2 for each row
  execute procedure trigger_func();