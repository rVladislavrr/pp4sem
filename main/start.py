from fastapi import FastAPI, HTTPException
from typing import Union, List
from neo4j import GraphDatabase
# from services.gener_math import req_math
from models.base import Exercise, Receipt
from config import *
from main.handling import filter_List, createListJson
from graph.graphDBCypher import behindFoo, nextFoo, pathFoo

app = FastAPI()
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

@app.on_event("startup")
async def startup():

    driver.verify_connectivity()


@app.get("/")
async def root(data: Union[List[Exercise], Receipt] = None):
    if isinstance(data, List):
        lst, flag = await filter_List(data)
        return await createListJson(driver, lst, flag)
    elif isinstance(data, Receipt):
        lst, flag = await filter_List(data.get_test())
        return await createListJson(driver, lst, flag, data.get_studied(), data.topic)
    elif not data:
        raise HTTPException(status_code=404, detail="None")
    else:
        raise HTTPException(status_code=400, detail="Invalid data type")


@app.get("/path/{start}/{end}")
async def path(start: str, end: str):
    return pathFoo(driver, start, end)


@app.get("/behind/{name_theme}")
async def behind(name_theme: str):
    return behindFoo(driver, name_theme)


@app.get("/next/{name_theme}")
async def nextpath(name_theme: str):
    return nextFoo(driver, name_theme)


@app.on_event("shutdown")
async def shutdown():
    driver.close()



