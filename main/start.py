from fastapi import FastAPI
from neo4j import GraphDatabase
# from services.gener_math import req_math
from models.base import ByReqvest
from config import *
from main.handling import filter_List, CreateResponse
from graph.graphDBCypher import behindFoo, nextFoo, pathFoo, getThemeByIdTask,createobj

app = FastAPI()
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


@app.on_event("startup")
async def startup():
    driver.verify_connectivity()

# @app.get("/api")
# async def root(data: Union[List[Exercise|Task], Receipt] = None):
#     if isinstance(data, List):
#         lst, flag = await filter_List(data)
#         return await createListJson(driver, lst, flag)
#     elif isinstance(data, Receipt):
#         lst, flag = await filter_List(data.get_test(driver))
#         return await createListJson(driver, lst, flag, data.get_studied(), data.topic)
#     elif not data:
#         raise HTTPException(status_code=404, detail="None")
#     else:
#         raise HTTPException(status_code=400, detail="Invalid data type")

@app.get("/api")
async def root(data:ByReqvest):
    lst, flag = await filter_List(data.get_test(driver))
    return await CreateResponse(driver, lst, flag, data.list_studied, data.topic)


@app.get("/api/id/{id_task}")
async def root(id_task:str):
    return getThemeByIdTask(id_task,driver)

@app.get("/api/path/{start}/{end}")
async def path(start: str, end: str):
    return list(map(lambda x:x.dict(), pathFoo(driver, start, end)))


@app.get("/api/behind/{name_theme}")
async def behind(name_theme: str):
    return list(map(lambda x:x.dict(), behindFoo(driver, name_theme)))


@app.get("/api/next/{name_theme}")
async def nextpath(name_theme: str):
    return list(map(lambda x:x.dict(), nextFoo(driver, name_theme)))


@app.get("/api/find_id/{name_theme}")
async def name_id(name_theme: str):
    return createobj(driver, name_theme)


@app.on_event("shutdown")
async def shutdown():
    driver.close()
