alter table "public"."orders" alter column "status" drop default;

alter table "public"."orders" alter column "status" set data type varchar using "status"::varchar;

drop type "public"."order_status";

create type "public"."order_status" as enum ('pending', 'processing', 'complete', 'rejected');

alter table "public"."orders" alter column "status" set data type order_status using "status"::order_status;

alter table "public"."orders" alter column "status" set default 'pending'::order_status;
