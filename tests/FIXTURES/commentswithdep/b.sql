CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value BIGINT
);

CREATE VIEW test_view AS
SELECT id, name, value
FROM test_table
WHERE value > 0;

COMMENT ON VIEW test_view IS 'This is a test view that shows positive values';
