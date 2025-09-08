# Frontend

This directory contains a minimal HTML interface for interacting with the
text editor backend. The page is served by FastAPI at the root URL and
provides controls to upload files, fetch from Bitbucket, create new
files, edit content, and save changes.

The interface exposes a top toolbar with **Home** and **File** menus. Use the
File menu to upload a file from your local machine or create a new file. Uploaded
files appear in the left sidebar where a context menu offers **Rename**,
**Open with editor**, and **Delete** actions.
