select
  nspname as schema,
  extname as name,
  extversion as version,
  e.oid as oid
from
    pg_extension e
    INNER JOIN pg_namespace
        ON pg_namespace.oid=e.extnamespace
order by schema, name;
