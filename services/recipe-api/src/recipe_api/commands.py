import subprocess
import sys


def dev_server() -> None:
    print("Starting development server...")
    cmd = [
        sys.executable, "-m", "uvicorn",
        "recipe_api.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8001"
    ]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nServer stopped")

def dev_worker() -> None:
    print("Starting worker with auto-reload...")
    cmd = [
        "watchmedo", "auto-restart",
        "--directory=src",
        "--pattern=*.py",
        "--recursive",
        "--",
        sys.executable, "-m", "recipe_api.workflows.worker"
    ]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nWorker stopped")
    except FileNotFoundError:
        print("Error: 'watchmedo' not found. Make sure 'watchdog' is installed (uv sync --extra dev).")
