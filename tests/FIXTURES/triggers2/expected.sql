DO
    $$
        BEGIN
            IF (SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'table2'
                  AND column_name = 't'
            ) THEN
                alter table "public"."table2" drop column "t";
            END IF;
        END
    $$;