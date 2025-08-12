CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    "None" INTEGER
);

COMMENT ON TABLE test_table IS 'This is a test table that still shows positive values';
