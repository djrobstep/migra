drop index if exists "public"."measurement_y2006m02_logdate_idx";

create table "public"."measurement_y2005m02" partition of "public"."measurement" FOR VALUES FROM ('2005-02-01') TO ('2005-03-01');


alter table "public"."measurement" detach partition "public"."measurement_y2006m03";

drop table "public"."partitioned2reg";

create table "public"."partitioned2reg" (
    "city_id" integer not null,
    "logdate" date not null,
    "peaktemp" integer,
    "unitsales" integer
);


drop table "public"."reg2partitioned";

create table "public"."reg2partitioned" (
    "city_id" integer not null,
    "logdate" date not null,
    "peaktemp" integer,
    "unitsales" integer
) partition by RANGE (logdate);


alter table "public"."measurement" add column "extra" text;
