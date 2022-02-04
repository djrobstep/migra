CREATE TABLE accounts (manager text, company text, contact_email text);

CREATE FUNCTION is_manager(manager text, out success boolean) returns boolean as $$
begin
    select manager = current_user into success;
end;
$$ language plpgsql stable;

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY account_managers_update ON accounts FOR UPDATE TO schemainspect_test_role
    USING (manager = current_user);

CREATE POLICY account_managers_insert ON accounts FOR INSERT TO schemainspect_test_role
    WITH CHECK (is_manager(manager));

CREATE TABLE accounts2 (manager text, company text, contact_email text);
