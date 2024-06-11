from fastapi import APIRouter, Query
from src.adaptive_logic.schemes import ByReq, Result, ThemeRes, ResultTask
from src.adaptive_logic.handling import create_res, create_task, get_name_id, get_id_name

router = APIRouter(
    tags=['Для создания ответных тестов'],
    prefix="/api",
)

des = """Принимаемая модель обычная: Основной параметр это 'test' состоит из объектов ( тема, задача) два 
дополнительных лист с изученными темами 'list_studied' и конечная тема 'topic', объект 'тема', 'задача' состоит из 
основных параметров: 'id' может быть листом строк, либо строкой, так же основной параметр, отвечающий за ответ, 
'answer' который даёт нам понять правильно ли решена задача или тема. Из дополнительного это сложность 'complexity', 
если её нет, объект будет рассматриваться как типовая задача, а 'id' должен быть соответсвующий задаче, в ином случае 
объект будет рассматриваться как тема, а 'id' тоже должен быть соответсвующий теме. Дополнительно можно посмотреть 
как выглядит объект внизу 'ByReq'"""


@router.post('/theme', description=des, name='Основной алгоритм с возращением тем')
async def main_foo(data: ByReq) -> Result:
    res, list_studied = await create_res(data)
    return Result(
        **{"tasks": [ThemeRes.model_validate(th, from_attributes=True) for th in res],
           "list_studied": list_studied})


@router.post('/task', description=des, name='Основной алгоритм с возращением задач')
async def main_foo_task(data: ByReq, ) -> ResultTask:
    res, list_studied = await create_res(data, True)
    return ResultTask(**{"tasks": create_task(res),
                         "list_studied": list_studied})


@router.get('/id/', name='Из id в имя', description='Id темы не задачи')
async def get_name(id_name: str = Query()) -> str:
    return get_name_id(id_name)


@router.get('/name/', name='Из имени в id', description="имя темы")
async def get_name(name: str = Query()) -> str:
    return get_id_name(name)
