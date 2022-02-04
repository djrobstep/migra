alter table "public"."t2" drop constraint "x";

alter table "public"."t2" drop constraint "t2_bb_fkey";

alter table "public"."t2" drop constraint "t2_pkey";

drop index if exists "public"."t1_a_idx";

drop index if exists "public"."t2_pkey";

alter table "public"."c" alter column "cc" set not null;

alter table "public"."t1" add column "price" numeric;

alter table "public"."t1" alter column "a" set not null;

DO
    $$
        BEGIN
            IF (SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 't2'
                  AND column_name = 'price'
            ) THEN
                alter table "public"."t2" drop column "price";
            END IF;
        END
    $$;

alter table "public"."t2" alter column "a" drop not null;

CREATE UNIQUE INDEX c_pkey ON public.c USING btree (cc);

CREATE UNIQUE INDEX t1_pkey ON public.t1 USING btree (a);

CREATE UNIQUE INDEX t2_a_idx ON public.t2 USING btree (a);

DO
    $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'c_pkey') THEN
                alter table "public"."c" add constraint "c_pkey" PRIMARY KEY using index "c_pkey" DEFERRABLE INITIALLY DEFERRED;
        END IF;
    END
$$;

DO
    $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 't1_pkey') THEN
                alter table "public"."t1" add constraint "t1_pkey" PRIMARY KEY using index "t1_pkey";
        END IF;
    END
$$;

DO
    $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'x') THEN
                alter table "public"."t1" add constraint "x" CHECK ((price > (0)::numeric));
        END IF;
    END
$$;

DO
    $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 't2_bb_fkey') THEN
                alter table "public"."t2" add constraint "t2_bb_fkey" FOREIGN KEY (bb) REFERENCES b(bb) DEFERRABLE INITIALLY DEFERRED;
        END IF;
    END
$$;