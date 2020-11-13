drop table "public"."t2";

create table "public"."t" (
    "id" integer not null,
    "a" text,
    "b" integer
);


CREATE UNIQUE INDEX t_pkey ON public.t USING btree (id);

alter table "public"."t" add constraint "t_pkey" PRIMARY KEY using index "t_pkey";

create or replace view "public"."v" as  SELECT t.id,
    t.a,
    max(t.b) AS max
   FROM t
  GROUP BY t.id;


create materialized view "public"."mv" as  SELECT v.id
   FROM v;


CREATE UNIQUE INDEX mv_id_idx ON public.mv USING btree (id);