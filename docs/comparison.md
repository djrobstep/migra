<div class="scroll-on-overflow full-width " markdown="1">
| Feature | migra | alembic | django |
| - | - | - | - |
| Migration files required for DB changes during dev? | No, autosyncs | Yes, required | Yes, required |
| Requires schema version number tracking | No version numbers involved | Yes, relies on version numbers | Yes, relies on version numbers |
| Must store entire chain of migration files? | No, only need one file with pending changes | Yes, required | Yes, required |
| ORMs supported | Supports any ORM or no ORM | SQLAlchemy ORM only | Django ORM only |
| Testability | Explicitly tests for matching schema | Doesn't test | Doesn't test |
| Needs copy of access to (copy of) current schema to generate migration scripts | Yes | No | No |
| Databases supported | PostgreSQL only | Postgres, mysql, various others | Postgres, mysql, various others |
</div>