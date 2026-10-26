"""Database schema and migrations management and initialization."""

from pathlib import Path
from app.database.connection import get_connection
# from app.utils.logger import Logger

# logger = Logger.get_logger(__name__)

# The index in "parents" array means to go up 2 folders,
# that in this case means the root of the project, where the "migrations" folder is located.
MIGRATIONS_DIRECTORY = Path(__file__).resolve().parents[2] / "migrations"

def initialize_database():
    """Initialize the database by applying any pending migrations."""

    # logger.info("Initializing database...")
    print("Initializing database...")
    with get_connection() as conn:
        # logger.info("Connected to the database.")
        print("Connected to the database.")
        with conn.cursor() as cursor:

            # logger.info("Initializing database schema by creating migration table...")
            print("Initializing database schema by creating migration table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # logger.info("Checking for applied migrations...")
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
            # logger.debug(f"Applied versions: {applied_versions}")
            print(f"Applied versions: {applied_versions}")

            migration_files = sorted(
                MIGRATIONS_DIRECTORY.glob("*.sql")
            )
            # logger.debug(f"Migration files: {migration_files}")
            print(f"Migration files: {migration_files}")

            for migration_file in migration_files:
                version = int(
                    migration_file.name.split("_")[0]
                )
                # logger.debug(f"Migration file: {migration_file.name} with version: {version}")
                print(f"Migration file: {migration_file.name} with version: {version}")

                # Check if all the migrations have already been applied
                # by checking if the version is the applied_versions set.
                # If it is, skip to the next migration.
                if version in applied_versions:
                    # logger.debug(f"Migration {migration_file.name} has already been applied.")
                    print(f"Migration {migration_file.name} has already been applied.")
                    continue

                sql = migration_file.read_text()

                # logger.debug(f"Applying migration {migration_file.name}")
                print(f"Applying migration {migration_file.name}")
                cursor.execute(sql)

                cursor.execute(
                    """
                    INSERT INTO schema_migrations (version)
                    VALUES (%s);
                    """,
                    (version,)
                )
                # logger.debug(f"Migration {migration_file.name} applied successfully.")
                print(f"Migration {migration_file.name} applied successfully.")
            # logger.info("Database initialization complete.")
            print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()
