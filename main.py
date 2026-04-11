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
    #resultDIctionary = dict()
    mycursor.execute("SELECT film_id, title, description, release_year FROM film WHERE film_id = %s;", (film_id,))
    query1 = mycursor.fetchone()
    mycursor.execute("SELECT ac.actor_id, CONCAT ( ac.first_name,' ', ac.last_name) AS actor_name " 
                    "from film flm "
                    "join film_actor fac on flm.film_id = fac.film_id "
                    "join actor ac on fac.actor_id = ac.actor_id " 
                    "where flm.film_id = %s;", (film_id,))
    query2 = mycursor.fetchall()
    result_dictionary = query1
    result_dictionary["actors"] = query2
    return result_dictionary


@app.get("/actors/{first_name}/{last_name}")
def view_actors(first_name: str, last_name: str):
    result_dictionary = dict()
    mycursor.execute("SELECT flm.film_id, flm.title "
                    "from actor ac "
                    "join film_actor fac on ac.actor_id = fac.actor_id "
                    "join film flm on fac.film_id = flm.film_id "
                    "where ac.first_name = %s and ac.last_name = %s; ", (first_name, last_name))
    film_query = mycursor.fetchall()
    mycursor.execute("SELECT ac.actor_id, CONCAT ( ac.first_name,' ', ac.last_name) AS actor_name "
                     "from actor ac "
                     "where ac.first_name = %s and ac.last_name = %s; ", (first_name, last_name))
    actor_query = mycursor.fetchall()
    result_dictionary["films"] = film_query
    result_dictionary["actor"] = actor_query
    return result_dictionary
## WHAT IF THERE WILL BE TWO IDENTICALLY NAMED ACTORS??


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
