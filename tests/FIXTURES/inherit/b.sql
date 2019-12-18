CREATE TABLE entity_bindings (
    id BIGSERIAL,
    entity_type TEXT NOT NULL,
    entity_id BIGINT NOT NULL
);
CREATE TABLE entity_bindings_A (
    CONSTRAINT "entity_type must be A" CHECK("entity_type" = 'A'),
    UNIQUE("entity_id", "entity_type")
) INHERITS (entity_bindings)
;
CREATE TABLE entity_bindings_B (
    CONSTRAINT "entity_type must be B" CHECK("entity_type" = 'B'),
    UNIQUE("entity_id", "entity_type")
) INHERITS (entity_bindings)
;
CREATE TABLE entity_bindings_C (
    CONSTRAINT "entity_type must be C" CHECK("entity_type" = 'C'),
    UNIQUE("entity_id", "entity_type")
) INHERITS (entity_bindings)
;