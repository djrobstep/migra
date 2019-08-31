with extension_oids as (
  select
      objid
  from
      pg_depend d
  WHERE
      d.refclassid = 'pg_extension'::regclass
) SELECT n.nspname AS schema,
   c.relname AS table_name,
   i.relname AS name,
   i.oid as oid,
   e.objid as extension_oid,
   pg_get_indexdef(i.oid) AS definition,
       (select string_agg(attname, ' ' order by attname) from pg_attribute where attnum = any(string_to_array(x.indkey::text, ' ')::int[]) and attrelid = x.indrelid) key_columns,
       indoption key_options, indnatts num_att, indisunique is_unique,
       indisprimary is_pk, indisexclusion is_exclusion, indimmediate is_immediate,
       indisclustered is_clustered, indcollation key_collations,
       pg_get_expr(indexprs, indrelid) key_expressions,
       pg_get_expr(indpred, indrelid) partial_predicate
  FROM pg_index x
    JOIN pg_class c ON c.oid = x.indrelid
    JOIN pg_class i ON i.oid = x.indexrelid
    LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
    left join extension_oids e
      on c.oid = e.objid or i.oid = e.objid
 WHERE c.relkind in ('r', 'm', 'p') AND i.relkind in ('i', 'I')
      -- SKIP_INTERNAL and nspname not in ('pg_catalog', 'information_schema', 'pg_toast')
      -- SKIP_INTERNAL and nspname not like 'pg_temp_%' and nspname not like 'pg_toast_temp_%'
      -- SKIP_INTERNAL and e.objid is null
order by 1, 2, 3;
