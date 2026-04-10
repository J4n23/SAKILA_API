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
def view_film(film_id: int = Path (description="Details of 1 film")):
    mycursor.execute("SELECT film_id, title, description, release_year FROM film WHERE film_id = %s;", (film_id,))
    result = mycursor.fetchone()
    return result


@app.get("/actors/{film_title}")
def view_actors(film_title: str):
    mycursor.execute("SELECT ac.first_name, ac.last_name " 
                    "from film flm "
                    "join film_actor fac on flm.film_id = fac.film_id "
                    "join actor ac on fac.actor_id = ac.actor_id " 
                    "where flm.title = %s;", (film_title,))
    result = mycursor.fetchall()
    return result

## DEMO OBJECT WITH NO PURPOSE
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
