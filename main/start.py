from fastapi import FastAPI, HTTPException
from typing import Union, List
from neo4j import GraphDatabase
# from services.gener_math import req_math
from models.base import *
from config import *

app = FastAPI()
app.driver = None

from main.handling import filter_List, createListJson


@app.on_event("startup")
async def startup():
    app.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    app.driver.verify_connectivity()


@app.get("/")
async def root(data: Union[List[Exercise], Receipt] = None):
    if isinstance(data, List):
        lst, flag = await filter_List(data)
        return await createListJson(lst, flag)
    elif isinstance(data, Receipt):
        lst, flag = await filter_List(data.get_test())
        return await createListJson(lst, flag, data.get_studied(), data.topic)
    elif not data:
        raise HTTPException(status_code=404, detail="None")
    else:
        raise HTTPException(status_code=400, detail="Invalid data type")


@app.get("/path/{start}/{end}")
async def path(start: str, end: str):
    with app.driver.session() as session:
        query = """MATCH path = shortestPath((start:theme {name: $name1})-[*]->(end:theme{name: $name2})) RETURN path"""
        res = list(session.run(query, name1=start, name2=end))
        if res:
            r = res[0]['path']
            return [dict(i)['name'] for i in r.nodes]
        return []


@app.get("/behind/{name_theme}")
async def behind(name_theme: str):
    with app.driver.session() as session:
        query = """MATCH (n:theme)-[:uses]->(:theme{name: $name2}) RETURN n"""
        res = list(session.run(query, name2=name_theme))
        if res:
            result = [dict(i['n'])['name'] for i in res]
            return list(set(result))
        return []


@app.get("/next/{name_theme}")
async def nextpath(name_theme: str):
    with app.driver.session() as session:
        query = """MATCH (:theme{name: $name2})-[:uses]->(n:theme) RETURN n"""
        res = list(session.run(query, name2=name_theme))
        if res:
            result = [dict(i['n'])['name'] for i in res]
            return list(set(result))
        return []


@app.on_event("shutdown")
async def shutdown():
    app.driver.close()



