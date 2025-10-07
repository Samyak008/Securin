# Recipe Data Parser

This project parses the US_recipes_null.json file and stores the recipe data in a SQLite database.

## Files

- `US_recipes_null.json`: Original JSON file containing 8,451 recipes
- `parse_recipes.py`: Script to parse the JSON and store in SQLite database
- `verify_database.py`: Script to verify the database contents
- `recipes.db`: SQLite database containing the parsed recipe data
- `query_examples.py`: Script with examples of how to query the database

## Database Schema

The SQLite database contains a single table called `recipes` with the following columns:

- `id`: TEXT PRIMARY KEY (the original JSON key)
- `continent`: TEXT
- `country_state`: TEXT
- `cuisine`: TEXT
- `title`: TEXT
- `url`: TEXT
- `rating`: REAL
- `total_time`: INTEGER
- `prep_time`: INTEGER
- `cook_time`: INTEGER
- `description`: TEXT
- `ingredients`: TEXT (JSON string)
- `instructions`: TEXT (JSON string)
- `nutrients`: TEXT (JSON string)
- `serves`: TEXT

## Usage

To run the parser:
```
python parse_recipes.py
```
