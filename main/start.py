from fastapi import FastAPI
# from services.gener_math import req_math
from models.base import Exercise
from main.handling import *

app = FastAPI()

@app.post("/")
async def root(data: list[Exercise]):
    lst, flag = await filter_List(data)
    # chek = createJsFgen(lst, flag)
    # print(req_math(chek))         возможность передавать уже сгенерированные задачи
    return await createJsFgen(lst, flag)

