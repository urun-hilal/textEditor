"""
file_editor.routes

Blueprint defining routes for file editing operations.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .utils import FILES_DIR, allowed_file, list_files

DEFAULT_FILENAME = "untitled.txt"

editor_bp = Blueprint("editor", __name__)


@editor_bp.route("/", methods=["GET", "POST"])
def index() -> str:
    """Render and process the file editing form.

    Returns:
        str: Rendered HTML for the editor or a redirect after saving.
    """
    if request.method == "POST":
        # Step 1: Retrieve filename and content
        filename = request.form.get("filename", DEFAULT_FILENAME)
        content = request.form.get("content", "")

        # Step 2: Validate file extension
        if not allowed_file(filename):
            flash("Unsupported file type.")
            return redirect(url_for("editor.index"))

        # Step 3: Save content to disk
        file_path = FILES_DIR / filename
        file_path.write_text(content, encoding="utf-8")
        flash(f"Saved {filename}.")
        return redirect(url_for("editor.index", filename=filename))

    # Step 4: Load file content if a filename is provided
    filename = request.args.get("filename")
    content = ""
    if filename and allowed_file(filename):
        file_path = FILES_DIR / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

    # Step 5: Render the page with existing files
    files = list_files()
    return render_template("editor.html", filename=filename or "", content=content, files=files)
