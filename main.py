from fastapi import FastAPI, Query
from typing import Optional
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.get('/recipes')
def get_recipes(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort_by: str = Query('title'),
    order: str = Query('asc')
):
    """
    Get all recipes with pagination and sorting
    """
    # Validate sort_by field to prevent SQL injection
    valid_sort_fields = ['cuisine', 'title', 'rating', 'prep_time', 'cook_time', 'total_time']
    if sort_by not in valid_sort_fields:
        sort_by = 'title'
    
    # Validate order
    order = order.upper()
    if order not in ['ASC', 'DESC']:
        order = 'ASC'
    
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    # Explicitly specify column names to ensure correct mapping
    recipes = conn.execute(
        f'SELECT cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves FROM recipes ORDER BY {sort_by} {order} LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    conn.close()
    
    recipes_list = [dict(recipe) for recipe in recipes]
    
    # Get total count for pagination info
    conn = get_db_connection()
    total_count = conn.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
    conn.close()
    
    return {
        'recipes': recipes_list,
        'page': page,
        'per_page': per_page,
        'total': total_count
    }

@app.get('/search')
def search_recipes(
    title: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    max_prep_time: Optional[int] = Query(None)
):
    """
    Search for recipes based on various fields
    """
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []
    
    if title:
        query += " AND title LIKE ?"
        params.append(f'%{title}%')
    
    if cuisine:
        query += " AND cuisine LIKE ?"
        params.append(f'%{cuisine}%')
    
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
    
    if max_prep_time is not None:
        query += " AND prep_time <= ?"
        params.append(max_prep_time)
    
    conn = get_db_connection()
    recipes = conn.execute(query, params).fetchall()
    conn.close()
    
    recipes_list = [dict(recipe) for recipe in recipes]
    
    return {'recipes': recipes_list}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)