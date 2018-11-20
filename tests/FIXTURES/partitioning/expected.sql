drop index if exists "public"."measurement_y2006m02_logdate_idx";

alter table "public"."measurement" detach partition "public"."measurement_y2006m03";

alter table "public"."measurement" add column "extra" text;
