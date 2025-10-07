import json
import sqlite3
from pathlib import Path

def create_database():
    """Create the SQLite database and table for storing recipes."""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Create the recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            cuisine TEXT,
            title TEXT,
            rating REAL,
            prep_time INTEGER,
            cook_time INTEGER,
            total_time INTEGER,
            description TEXT,
            nutrients JSONB,
            serves TEXT
        )
    ''')
    
    conn.commit()
    return conn

def parse_and_store_recipes():
    """Parse the JSON file and store the data in the database."""
    # Read the JSON file
    with open('US_recipes_null.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Connect to database
    conn = create_database()
    cursor = conn.cursor()
    
    # Process each recipe in the JSON data
    for key, recipe in data.items():
        cursor.execute('''
            INSERT OR REPLACE INTO recipes 
            (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe.get('cuisine'),
            recipe.get('title'),
            recipe.get('rating'),
            recipe.get('prep_time'),
            recipe.get('cook_time'),
            recipe.get('total_time'),
            recipe.get('description'),
            json.dumps(recipe.get('nutrients')),
            recipe.get('serves')
        ))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Successfully stored {len(data)} recipes in the database.")

if __name__ == "__main__":
    print("Starting to parse and store recipes...")
    parse_and_store_recipes()
    print("Completed storing recipes in the database.")