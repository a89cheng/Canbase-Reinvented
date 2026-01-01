# Canbase Reinvented: A Chess Database Project | Dec, 13 2025 - Present

## Overview

This project is a **from-scratch chess database system** built to demonstrate core software engineering skills: domain modeling, parsing, relational database design, SQL querying, and Python–SQL integration.

The system ingests chess games from PGN files (from but not limited to the Canadian chess Database "Canbase"), normalizes them into a relational schema, and provides query-based analytics on players, tournaments, games, and openings.

This repository reflects progress **up to the current phase** (with continued work on the project), where the database is fully populated and basic analytics queries are implemented.

---

## Project Goals

* Design a clean, normalized relational database for chess data
* Replace ad-hoc data structures with explicit domain models
* Safely ingest and validate real-world PGN data
* Practice raw SQL (no ORMs) and Python–SQL interaction
* Generate meaningful analytics from stored game data
* Maintain testability, clarity, and extensibility throughout

---

## Current Capabilities

At this stage, the project supports:

### PGN Parsing & Domain Modeling

* Parsing PGN files into structured Python objects
* A `Game` domain model that:

  * Owns and validates game metadata
  * Enforces a consistent internal structure
  * Replaces dictionary-based data handling

### Database Breakdown

* Relational schema with the following core tables:
  * `Player`
  * `Tournament`
  * `Game`
* Proper use of primary keys and foreign keys
* No duplicated or denormalized data

### Data Insertion Pipeline

* Deterministic insert functions for each table
* Duplicate prevention and integrity checks
* Explicit handling of missing or partial metadata

### SQL Querying & Analytics

* Aggregate queries across multiple tables
* Examples include:

  * Total games stored
  * Most common openings (ECO codes)
  * Games played per player
* Results formatted cleanly for display or further processing

---

## Project Structure

```
src/
├── models/        # Domain models (e.g. Game)
├── parser/        # PGN parsing logic
├── db/            # Schema setup and insert/query functions
├── analytics/     # SQL analytics and aggregation queries
├── app.py         # Entry point / driver script

tests/             # Pytest-based automated tests
```

---

## Design Principles

* **Explicit over implicit**: clear data ownership and responsibilities
* **Minimal abstraction**: raw SQL over ORMs to build fundamentals
* **Incremental complexity**: features added only when justified
* **Test-first mindset**: functionality validated through automated tests

---

## What I'm Working On Next...

The following are intentionally excluded at this stage:

* Chess engine analysis
* Move-by-move validation or evaluation
* Web interfaces or APIs
* Performance optimization beyond correctness

These are considered future expansion points, not omissions.

---

## App Status

✔ Database schema complete
✔ PGN parsing stable
✔ Data insertion validated
✔ Core analytics queries implemented

The project is now positioned for **deeper analytics, schema extensions, and more advanced querying** in future phases.
