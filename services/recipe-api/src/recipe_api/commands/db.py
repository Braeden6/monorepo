import subprocess
import sys


def generate() -> None:
    if len(sys.argv) < 2:
        print("Error: Migration message required.")
        print("Usage: uv run dev-migrate \"message\"")
        sys.exit(1)

    message = sys.argv[1]
    print(f"Creating migration with message: {message}")

    cmd = [
        sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", message
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMigration stopped")
        sys.exit(1)

def migrate() -> None:
    print("Updating database...")
    cmd = [sys.executable, "-m", "alembic", "upgrade", "head"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDatabase update stopped")
        sys.exit(1)
