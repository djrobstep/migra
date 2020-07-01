drop table "public"."unwanted";

alter sequence "public"."test2_id_seq" owned by "public"."test2"."id";

alter sequence "public"."test_id_seq" owned by none;

