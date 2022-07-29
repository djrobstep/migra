create table b(bb int primary key);

create table t2(a int, bb int references b(bb) DEFERRABLE INITIALLY deferred);

create table t1(a int primary key, price numeric, constraint x check (price > 0));

create table c(cc int unique);

CREATE UNIQUE INDEX c_pkey ON public.c USING btree (cc);

alter table "public"."c" add constraint "c_pkey" PRIMARY KEY using index "c_pkey" deferrable INITIALLY deferred;

create unique index on t2(a);

CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);

CREATE TABLE circles_dropexclude (
    c circle
);