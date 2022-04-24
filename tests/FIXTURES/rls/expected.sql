drop policy "account_managers_insert" on "public"."accounts";

drop policy "account_managers_update" on "public"."accounts";

alter table "public"."accounts2" enable row level security;

create policy "account_managers_insert"
on "public"."accounts"
as restrictive
for insert
to schemainspect_test_role
with check (is_manager(manager));


create policy "account_managers_update"
on "public"."accounts"
as restrictive
for update
to schemainspect_test_role
using ((manager = CURRENT_USER));


