CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value INTEGER,
    "None" TEXT
);

CREATE VIEW test_view AS
SELECT id, name, value
FROM test_table
WHERE value > 0;

COMMENT ON VIEW test_view IS 'This is a test view that shows positive values';

COMMENT ON COLUMN test_view.id IS 'Unique identifier from test_table';
