DO
    $$
        BEGIN
            IF (SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'timestamp_base'
                  AND column_name = 'e'
            ) THEN
                alter table "public"."timestamp_base" drop column "e";
            END IF;
        END
    $$;

DO
    $$
        BEGIN
            IF (SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'a'
                  AND column_name = 'a2'
            ) THEN
                alter table "public"."a" drop column "a2";
            END IF;
        END
    $$;

alter table "public"."a" add column "e" integer;


