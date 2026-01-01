# How to Run Chess Database Project

## 1. Prerequisites

* **Python 3.10 or higher**
* Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

> Note: SQLite is included in Python standard library, no extra installation needed.

## 2. Project Structure

Ensure your project folder has:

```
src/
tests/
requirements.txt
README.md
PGN_files/   # put your PGN files here
```

## 3. Running the Application

1. Open terminal in the project root.
2. Run the main app script:

```bash
python src/app.py
```

3. The script will:

   * Parse PGN files in `PGN_files/`
   * Insert data into the SQLite database
   * Print basic analytics to the console

## 4. Running Tests

Automated tests are written with `pytest`. Run them with:

```bash
pytest
```

All tests validate:

* Parsing correctness
* Database inserts
* Analytics query outputs

## 5. Notes

* Database file will be created automatically if not present.
* Make sure PGN files are valid; invalid files will be skipped.
* Analytics queries can be extended in `src/analytics/`.

---

You are now ready to run, test, and extend the Chess Database project.
