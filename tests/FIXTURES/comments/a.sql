CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value INTEGER,
    "None" TEXT
);

COMMENT ON TABLE test_table IS 'This is a test table that shows positive values';

COMMENT ON COLUMN test_table.id IS 'Unique identifier from test_table';