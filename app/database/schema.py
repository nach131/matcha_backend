from pathlib import Path
from app.database.connection import get_connection

# Directory where migration SQL files are stored
MIGRATIONS_DIRECTORY = Path(__file__).parent / "migrations"

# Database initialization
def initialize_database():

    # Get database connection from connection pool
    with get_connection() as conn:
        print("Connected to the database.")
        with conn.cursor() as cursor:

            # Handle schema migrations table creation
            print("Initializing database schema...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Check for applied migrations
            print("Checking for applied migrations...")
            cursor.execute("""
                SELECT version
                FROM schema_migrations
                ORDER BY version;
            """)

            applied_versions = {
                row["version"]
                for row in cursor.fetchall()
            }

            migration_files = sorted(
                MIGRATIONS_DIRECTORY.glob("*.sql")
            )

            for migration_file in migration_files:

                print("Migration file: ", migration_file.name)
                version = int(
                    migration_file.name.split("_")[0]
                )

                # Check if all the migrations have already been applied
                # by checking if the version is the applied_versions set.
                # If it is, skip to the next migration.
                if version in applied_versions:
                    print(f"Migration {migration_file.name} has already been applied.")
                    continue

                sql = migration_file.read_text()

                # TODO: Add logger function
                print(
                    f"Applying migration "
                    f"{migration_file.name}"
                )

                cursor.execute(sql)

                cursor.execute(
                    """
                    INSERT INTO schema_migrations (version)
                    VALUES (%s);
                    """,
                    (version,)
                )
                print(f"Migration {migration_file.name} applied successfully.")

if __name__ == "__main__":
    initialize_database()
