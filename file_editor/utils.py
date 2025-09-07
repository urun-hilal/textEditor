"""
file_editor.utils

Helper functions for file validation and discovery.
"""

from pathlib import Path
from typing import List

ALLOWED_EXTENSIONS = {"yaml", "yml", "json", "txt"}
BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = BASE_DIR / "files"
FILES_DIR.mkdir(exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Determine if the file extension is permitted.

    Args:
        filename (str): Name of the file to validate.

    Returns:
        bool: True when the extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def list_files() -> List[str]:
    """List existing editable files in the storage directory.

    Returns:
        List[str]: Names of files with allowed extensions.
    """
    # Step 1: Scan the files directory
    paths = FILES_DIR.iterdir()

    # Step 2: Filter by allowed extensions
    files = [p.name for p in paths if p.suffix.lstrip(".") in ALLOWED_EXTENSIONS]
    return files
