# Base de données

- `db_client.py`: client SQLAlchemy (SQLite par défaut)
- `schema.sql`: schéma minimal (table `persons`)

Initialisation (SQLite):

```bash
python -m app.db.db_client --init-db
```