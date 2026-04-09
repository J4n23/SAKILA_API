from fastapi import FastAPI, HTTPException, Path
from database import mydb, mycursor


app = FastAPI(
    title="Sakila Training Project"
)

@app.get("/categories/")
def list_categories():
    mycursor.execute("SELECT * FROM category")
    categories_result = mycursor.fetchall()
    return categories_result


@app.get("/films/")
def list_films():
    mycursor.execute("SELECT film_id, title, release_year FROM film")
    film_result = mycursor.fetchall()
    return film_result


@app.get("/films/{film_id}")
def view_film(film_id: int = Path (description="Details of 1 film", examples="3")):
    mycursor.execute("SELECT film_id, title, description, release_year FROM film WHERE film_id = %s;", (film_id,))
    result = mycursor.fetchone()
    return result


@app.get("/actors/{film_title}")
def view_actors(film_title: str):
    mycursor.execute("SELECT actor.first_name, actor.last_name" 
                    "from film join film_actor on film.film_id = film_actor.film_id"
                    "join actor on film_actor.actor_id = actor.actor_id where film.title = %s;", (film_title,))
    result = mycursor.fetchall()
    return result


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
