create sequence "public"."entity_bindings_id_seq";

drop table "public"."t";

create table "public"."entity_bindings" (
    "id" bigint not null default nextval('entity_bindings_id_seq'::regclass),
    "entity_type" text not null,
    "entity_id" bigint not null
);


create table "public"."entity_bindings_a" (
    "id" bigint not null default nextval('entity_bindings_id_seq'::regclass),
    "entity_type" text not null,
    "entity_id" bigint not null
) inherits ("public"."entity_bindings");


create table "public"."entity_bindings_b" (
    "id" bigint not null default nextval('entity_bindings_id_seq'::regclass),
    "entity_type" text not null,
    "entity_id" bigint not null
) inherits ("public"."entity_bindings");


create table "public"."entity_bindings_c" (
    "id" bigint not null default nextval('entity_bindings_id_seq'::regclass),
    "entity_type" text not null,
    "entity_id" bigint not null
) inherits ("public"."entity_bindings");


alter sequence "public"."entity_bindings_id_seq" owned by "public"."entity_bindings"."id";

CREATE UNIQUE INDEX entity_bindings_a_entity_id_entity_type_key ON public.entity_bindings_a USING btree (entity_id, entity_type);

CREATE UNIQUE INDEX entity_bindings_b_entity_id_entity_type_key ON public.entity_bindings_b USING btree (entity_id, entity_type);

CREATE UNIQUE INDEX entity_bindings_c_entity_id_entity_type_key ON public.entity_bindings_c USING btree (entity_id, entity_type);

alter table "public"."entity_bindings_a" add constraint "entity_bindings_a_entity_id_entity_type_key" UNIQUE using index "entity_bindings_a_entity_id_entity_type_key";

alter table "public"."entity_bindings_a" add constraint "entity_type must be A" CHECK ((entity_type = 'A'::text)) not valid;

alter table "public"."entity_bindings_a" validate constraint "entity_type must be A";

alter table "public"."entity_bindings_b" add constraint "entity_bindings_b_entity_id_entity_type_key" UNIQUE using index "entity_bindings_b_entity_id_entity_type_key";

alter table "public"."entity_bindings_b" add constraint "entity_type must be B" CHECK ((entity_type = 'B'::text)) not valid;

alter table "public"."entity_bindings_b" validate constraint "entity_type must be B";

alter table "public"."entity_bindings_c" add constraint "entity_bindings_c_entity_id_entity_type_key" UNIQUE using index "entity_bindings_c_entity_id_entity_type_key";

alter table "public"."entity_bindings_c" add constraint "entity_type must be C" CHECK ((entity_type = 'C'::text)) not valid;

alter table "public"."entity_bindings_c" validate constraint "entity_type must be C";