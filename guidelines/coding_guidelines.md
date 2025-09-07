# Coding Guidelines

These guidelines ensure readability, maintainability, and consistency across the codebase. Please follow them strictly when writing or modifying code.

---

## 1. Code Style

### File Structure
1. **Module-Level Docstring**
   - Start every file with a concise docstring describing:
     - The purpose of the module.
     - Key classes or functions provided.
     - Any special notes (dependencies, limitations, etc.).
   - Example:
     ```python
     """
     utils.py

     Utility functions for string processing, file I/O, and logging.
     These functions are shared across multiple modules.
     """
     ```

2. **Imports**
   - Place all imports directly below the module docstring.
   - Group imports in the following order (with a blank line between groups):
     1. Standard library
     2. Third-party libraries
     3. Local modules
   - Example:
     ```python
     import os
     import sys

     import requests
     import pandas as pd

     from project.utils import format_date
     ```

3. **Constants & Globals**
   - Define module-level constants (UPPER_CASE) and global variables after imports.
   - Avoid using mutable global variables.
   - Example:
     ```python
     DEFAULT_TIMEOUT = 30
     API_VERSION = "v1"
     ```

4. **Functions and Classes**
   - Define all functions and classes **after constants/globals**.
   - Test functions (if included in the same file) should be placed at the bottom.

5. **Entry Point**
   - End the file with:
     ```python
     if __name__ == "__main__":
         main()
     ```
   - Only include this if the module is intended to run as a script.

---

### Function & Class Style
1. **Docstrings**
   - Every function and class must include a docstring.
   - Docstrings should explain:
     - Purpose of the function/class.
     - Parameters with types.
     - Return type.
   - Example:
     ```python
     def calculate_area(radius: float) -> float:
         """
         Calculate the area of a circle.

         Args:
             radius (float): Radius of the circle.

         Returns:
             float: The calculated area.
         """
         return 3.14159 * radius ** 2
     ```

2. **Type Annotations**
   - Always annotate parameter and return types.
   - Use `Optional`, `List`, `Dict`, etc. from `typing` where needed.

3. **Comments for Macro Steps**
   - Inside each function, identify logical sections (macro steps).
   - Add a one-line comment describing the intent of each macro step.
   - Example:
     ```python
     def process_data(file_path: str) -> pd.DataFrame:
         """
         Load, clean, and transform data from a CSV file.
         """
         # Step 1: Load the data
         df = pd.read_csv(file_path)

         # Step 2: Clean missing values
         df = df.dropna()

         # Step 3: Apply transformations
         df["processed_date"] = pd.to_datetime(df["date"])

         return df
     ```
   - If a function is short and doesn’t require splitting, one comment or none is acceptable.

---

## 2. Maintenance

1. **Updating Docstrings**
   - Whenever modifying a function, class, or file:
     - Update the corresponding docstring.
     - Ensure type hints are accurate.

2. **Dependencies**
   - Keep `requirements.txt` updated whenever:
     - Adding a new package.
     - Removing unused packages.
   - Use `pip freeze > requirements.txt` responsibly (remove unnecessary dev-only packages).

3. **.gitignore**
   - Update `.gitignore` to exclude:
     - Temporary files (`*.log`, `*.tmp`, etc.).
     - Build artifacts.
     - Virtual environments (`venv/`, `.env/`).
     - System-specific files (`.DS_Store`, `Thumbs.db`).

---

## 3. General Best Practices

1. **Naming Conventions**
   - Variables & functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_CASE`
   - Private/internal functions: `_leading_underscore`

2. **Code Length**
   - Keep functions small and focused (prefer < 40 lines).
   - Split complex logic into helper functions.

3. **Error Handling**
   - Use exceptions, not return codes, for error handling.
   - Catch specific exceptions, not generic `Exception`.

---