import mysql.connector
from fastapi import FastAPI, HTTPException, Path
from database import mydb, mycursor
from pydantic import BaseModel
from typing import List, Optional, Literal

# from mysql.connector.errors import Error


app = FastAPI(
    title="Sakila Training Project"
)

class Category(BaseModel):
    category_id: int
    name: str

class Film(BaseModel):
    film_id: int
    title: str
    release_year: Optional[int] = None

class Actor(BaseModel):
    actor_id: int
    actor_name: str

class FilmDetail(BaseModel):
    film_id: int
    title: str
    description: str
    release_year: int
    actors: List[Actor]



class Availability(BaseModel):
    AVAILABLE: int

@app.get("/categories/", response_model=List[Category])
def list_categories():
    try:
        mycursor.execute("SELECT category_id, name FROM category")
        categories_result = mycursor.fetchall()
        return categories_result
    except mysql.connector.Error as err:
        raise HTTPException(status_code=503, detail=str(err))


@app.get("/films/", response_model=List[Film])
def list_films(
        limit: int=100,
        offset: int=0,
        sort_by: Literal["film_id", "title", "release_year"]= "film_id",
        order_by: Literal["asc", "desc"] = "asc"
):
    try:
        query = "SELECT film_id, title, release_year FROM film"+" ORDER BY " + sort_by + " " + order_by + ";"

        mycursor.execute(query)
        film_result = mycursor.fetchall()
        return film_result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=503, detail=str(err))
# TODO: Implement sorting and pagination into query

@app.get("/films/{film_id}", response_model=FilmDetail)
def view_film(film_id: int = Path (description="Details of 1 film")):
    try:
        mycursor.execute("SELECT film_id, title, description, release_year FROM film WHERE film_id = %s;", (film_id,))
        query1 = mycursor.fetchone()
        if query1:
            mycursor.execute("SELECT ac.actor_id, CONCAT ( ac.first_name,' ', ac.last_name) AS actor_name " 
                            "from film flm "
                            "join film_actor fac on flm.film_id = fac.film_id "
                            "join actor ac on fac.actor_id = ac.actor_id " 
                            "where flm.film_id = %s;", (film_id,))
            query2 = mycursor.fetchall()
            result_dictionary = query1
            result_dictionary["actors"] = query2
            return result_dictionary
        else:
            raise HTTPException(status_code=404, detail="Film ID Not Found!")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=503, detail=str(err))


@app.get("/actors/{first_name}/{last_name}", response_model=List[Film])
def view_actors(first_name: str, last_name: str):
    try:
        mycursor.execute("SELECT ac.actor_id, CONCAT ( ac.first_name,' ', ac.last_name) AS actor_name "
                         "from actor ac "
                         "where ac.first_name = %s and ac.last_name = %s; ", (first_name, last_name))
        actor_query = mycursor.fetchall()
        if actor_query:
            mycursor.execute("SELECT flm.film_id, flm.title, flm.release_year "
                            "from actor ac "
                            "join film_actor fac on ac.actor_id = fac.actor_id "
                            "join film flm on fac.film_id = flm.film_id "
                            "where ac.first_name = %s and ac.last_name = %s; ", (first_name, last_name))
            film_query = mycursor.fetchall()
            result_dictionary = film_query
            return result_dictionary
        else:
            raise HTTPException(status_code=404, detail="No Such Actor In Database!")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=503, detail=str(err))


@app.get("/inventory/{film_id}", response_model=Availability)
def view_availability(film_id: int):
    try:
        mycursor.execute("SELECT EXISTS (SELECT inventory_id FROM inventory WHERE film_id = %s);", (film_id,))
        alive = mycursor.fetchone()
        if alive:
            mycursor.execute("SELECT COUNT(result.inventory_id) AS AVAILABLE "
                            "FROM ( "
                                "SELECT DISTINCT rnt.inventory_id, inv.film_id "
                                "FROM inventory inv "
                                "JOIN rental rnt ON inv.inventory_id = rnt.inventory_id " 
                                "WHERE inv.film_id = %s "
                                "AND rnt.inventory_id NOT IN (SELECT inventory_id from rental where return_date is NULL) "
                            ") AS result; ", (film_id, ))
            availability = mycursor.fetchone()
            return availability
        else:
            raise HTTPException(status_code=404, detail="No Such Movie In Inventory!")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=503, detail=str(err))


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
