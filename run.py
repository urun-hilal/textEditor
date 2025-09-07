"""
run

Entry point for running the file editor web application.
"""

from file_editor import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
