with extension_oids as (
  select
      objid
  from
      pg_depend d
  WHERE
      d.refclassid = 'pg_extension'::regclass
)
SELECT n.nspname as "schema",
  substr(pg_catalog.format_type(t.oid, NULL), strpos(pg_catalog.format_type(t.oid, NULL), '.') + 1) AS "name",
  ARRAY(
     SELECT e.enumlabel
      FROM pg_catalog.pg_enum e
      WHERE e.enumtypid = t.oid
      ORDER BY e.enumsortorder
  ) as elements
FROM pg_catalog.pg_type t
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
     left outer join extension_oids e
       on t.oid = e.objid
WHERE
  t.typcategory = 'E'
  and e.objid is null
  -- SKIP_INTERNAL and n.nspname not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
  -- SKIP_INTERNAL and n.nspname not like 'pg_temp_%' and n.nspname not like 'pg_toast_temp_%'
ORDER BY 1, 2;
