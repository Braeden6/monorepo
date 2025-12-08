import subprocess
import sys


def _run_pytest(test: list[str]) -> None:
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments, example: uv run test src/recipe_api/features/health")
    if len(sys.argv) > 1:
        test = test + sys.argv[1:]
    cmd = [sys.executable, "-m", "pytest"] + test
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTests stopped")
        sys.exit(1)

def all_tests() -> None:
    _run_pytest([])

def unit_tests() -> None:
    _run_pytest(["-m", "unit"])

def e2e_tests() -> None:
    _run_pytest(["-m", "e2e"])
