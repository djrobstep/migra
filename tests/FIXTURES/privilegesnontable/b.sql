create table test_table(id integer primary key, value text);

create view test_view as select * from test_table;

create sequence test_sequence;

create function test_function() returns integer as $$
    begin
        return 1;
    end;
$$ language plpgsql;

grant select(id) on test_table to schemainspect_test_role2;
grant execute on function test_function() to schemainspect_test_role2;
