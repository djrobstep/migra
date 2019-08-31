select
    sequence_schema as schema,
    sequence_name as name
from information_schema.sequences
-- SKIP_INTERNAL where sequence_schema not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
-- SKIP_INTERNAL and sequence_schema not like 'pg_temp_%' and sequence_schema not like 'pg_toast_temp_%'
order by 1, 2;
