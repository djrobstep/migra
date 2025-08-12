create table test_table(id integer primary key, value text);

create view test_view as select * from test_table;

create sequence test_sequence;

create function test_function() returns integer as $$
    begin
        return 1;
    end;
$$ language plpgsql;

grant select on test_view to schemainspect_test_role;
grant usage on test_sequence to schemainspect_test_role;
grant select(value) on test_table to schemainspect_test_role;
grant execute on function test_function() to schemainspect_test_role; 