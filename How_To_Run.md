# How to Run Chess Database Project

## 1. Prerequisites

* **Python 3.10 or higher**
* **MySQL 8.0 or higher** — [Download here](https://dev.mysql.com/downloads/)
* Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

> `requirements.txt` should include `mysql-connector-python` (or `PyMySQL`) in addition to other project dependencies.

---

## 2. MySQL Setup

### 2a. Create the Database and User

Log into MySQL as root:

```bash
mysql -u root -p
```

Then run:

```sql
CREATE DATABASE chess_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chess_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON chess_db.* TO 'chess_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2b. Configure the Connection

Create a `.env` file in the project root (or update `src/config.py`) with your connection details:

```
DB_HOST=localhost
DB_PORT=3306 (The default MySQL port)                
DB_NAME=Canbase_Reinvented (Keep this please!)
DB_USER=chess_user
DB_PASSWORD=your_password
```

> **Never commit your `.env` file to version control.** Add it to `.gitignore`.

---

## 3. Project Structure

Ensure your project folder has:

```
src/
tests/
requirements.txt
README.md
PGN_files/   # some sample pgns here
.env         # MySQL credentials (not committed)
```

---

## 4. Running the Application

1. Make sure your MySQL server is running.
2. Open a terminal in the project root.
3. Run the main app script:

```bash
streamlit run app.py
```

The script will:

* Parse PGN files in `PGN_files/`
* Connect to the MySQL database using your `.env` credentials
* Create tables if they don't already exist
* Insert game data into the database
* Print basic analytics to the console

---

## 5. Running Tests

Automated tests are written with `pytest`. Before running, ensure your test database is configured (you may want a separate `chess_db_test` database to avoid polluting production data).

Run tests with:

```bash
pytest
```

All tests validate:

* Parsing correctness
* Database inserts
* Analytics query outputs

---

## 6. Notes

* Tables will be created automatically on first run if they don't exist.
* Make sure PGN files are valid; invalid files will be skipped.
* Analytics queries can be extended in `src/analytics/`.
* MySQL is stricter than SQLite about data types and constraints — ensure your schema uses `VARCHAR`, `TEXT`, `INT`, and `DATETIME` types appropriately.
* If you see `Access denied` errors, double-check your `.env` credentials and that the MySQL user has been granted the correct privileges.

---

You are now ready to run, test, and extend the Chess Database project with MySQL.