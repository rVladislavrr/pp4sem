from fastapi import APIRouter
from src.adaptive_logic.schemes import ByReq, Result
from src.adaptive_logic.handling import create_with_neg, create_positive

router = APIRouter(
    tags=['Для создания задач'],
    prefix="/api",
)
@router.post('')
async def main_foo(data: ByReq) -> Result:
    test, count = data.get_test()
    negative = [mod for mod in test if not mod.answer]
    positive = [mod for mod in test if mod.answer]

    if negative:
        res = await create_with_neg(negative, positive,count, data.list_studied, data.topic)
        return res
    return await create_positive(positive,count, data.list_studied, data.topic)