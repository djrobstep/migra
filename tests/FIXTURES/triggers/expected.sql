drop trigger if exists "emp_stamp_drop" on "public"."emp";

drop trigger if exists "emp_stamp" on "public"."emp";

CREATE TRIGGER emp_stamp_create BEFORE INSERT OR UPDATE ON public.emp FOR EACH ROW EXECUTE FUNCTION emp_stamp();

CREATE TRIGGER emp_stamp BEFORE UPDATE ON public.emp FOR EACH ROW EXECUTE FUNCTION emp_stamp();
