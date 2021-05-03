DO
$$
    BEGIN
        IF (SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'any_table'
        ) THEN
            REVOKE delete on table "public"."any_table" from "postgres";
        END IF;
    END
$$;

drop view if exists "public"."any_other_view";

grant update on table "public"."any_table" to "postgres";
