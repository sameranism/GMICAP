# DATABASE_REVIEW - proposal review and migration plan

- **Task:** `S00-016`  
- **Input:** `database_dictionary.csv` (41 proposed tables), 3 proposal SQL files
- **Status:** review record, **not executable DDL**. No proposal SQL has been run against any database.

## Tables per package

| Package | Tables |
|---|---:|
| B01 | 12 |
| B02 | 3 |
| B03 | 3 |
| B04 | 4 |
| B05 | 5 |
| B06 | 6 |
| B07 | 2 |
| B08 | 4 |
| B09 | 2 |

## Physical placement

| Location | Tables |
|---|---:|
| هسته مرکزی | 34 |
| سرور داخلی | 3 |
| سرور خارجی | 3 |
| مخزن محرمانه مجزا | 1 |

## Findings

1. **Duplicate table names:** 0 (none).
2. **Credential-bearing columns that must never store plaintext** (hash or `credential_ref` only):

   - `identity.users`: user_id, username, role_id, password_hash, must_reset, is_active, created_at
   - `publish.destinations`: destination_id, provider, channel_ref, stream, desk, credential_ref, verified
3. **Cross-database references:** the dictionary must not contain foreign keys across the three
   databases; ownership is by package and joins happen through contracts, not tables.
4. **Unsafe defaults:** no `DEFAULT 'admin'`, no seeded password, no `GRANT ALL` in migrations.
5. **Proposal SQL is evidence only:** `postgres_central_schema_PROPOSAL.sql` and the domestic/foreign
   proposals must not be executed directly; they are the source for reviewed Alembic revisions.

## Migration plan (not yet executed)

1. Write `backend/migrations/central/001_baseline.py` from the reviewed subset of the central proposal.
2. Domestic and foreign baselines live under their own migration roots (separate databases).
3. Run each revision forward and backward on a throwaway PostgreSQL instance; record the log.
4. Only then allow staging; production migration requires the client's maintenance window.
5. Every migration is append-only; edits after merge need a new revision.

## Open questions

- Backup policy and retention per database.
- Whether the three databases share a host in phase 1 (recommended) or are separated.
- Which objects belong in object storage versus the archive record.
