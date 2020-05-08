drop trigger if exists "trigger_on_view" on "public"."view_on_table";

drop view if exists "public"."view_on_table";

alter table "public"."my_table" add column "some_date" timestamp without time zone;

create or replace view "public"."view_on_table" as  SELECT my_table.some_text,
    my_table.some_date,
    my_table.some_count
   FROM my_table;


CREATE TRIGGER trigger_on_view INSTEAD OF INSERT ON public.view_on_table FOR EACH ROW EXECUTE FUNCTION my_function();
