import json
import subprocess
from pathlib import Path

from recipe_api.main import app


def generate() -> None:
    openapi_data = app.openapi()

    root_dir = Path(__file__).parent.parent.parent.parent
    openapi_path = root_dir / "openapi.json"
    output_path = root_dir / "tests" / "api_client"

    openapi_path.write_text(json.dumps(openapi_data, indent=2))

    if output_path.exists():
        pass

    cmd = [
        "uv", "run", "openapi-python-client", "generate",
        "--path", str(openapi_path),
        "--output-path", str(output_path),
        "--overwrite"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)

        # Cleanup unwanted generated files
        for filename in ["README.md", "pyproject.toml", ".gitignore"]:
            file = output_path / filename
            if file.exists():
                file.unlink()
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        if openapi_path.exists():
            openapi_path.unlink()

    print("Successfully generated client!")
