alter table "public"."orders" alter column "status" drop default;

alter type "public"."order_status" rename to "order_status__old_version_to_be_dropped";

create type "public"."order_status" as enum ('pending', 'processing', 'complete', 'rejected');

alter table "public"."orders" alter column status type "public"."order_status" using status::text::"public"."order_status";

alter table "public"."orders" alter column "status" set default 'pending'::order_status;

drop type "public"."order_status__old_version_to_be_dropped";

alter table "public"."orders" alter column "othercolumn" set data type other.otherenum2 using "othercolumn"::text::other.otherenum2;
