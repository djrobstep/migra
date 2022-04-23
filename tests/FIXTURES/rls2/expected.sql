create sequence "public"."example_id_seq";

drop table "public"."t";

create table "public"."example" (
    "id" integer not null default nextval('example_id_seq'::regclass),
    "name" text not null
);


alter table "public"."example" enable row level security;

alter sequence "public"."example_id_seq" owned by "public"."example"."id";

CREATE UNIQUE INDEX example_pkey ON public.example USING btree (id);

alter table "public"."example" add constraint "example_pkey" PRIMARY KEY using index "example_pkey";

create policy "example_all"
on "public"."example"
as permissive
for all
to public
using (true);