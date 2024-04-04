from fastapi import FastAPI
# from services.gener_math import req_math
from models.base import Exercise

app = FastAPI()


@app.post("/")
async def root(data: list[Exercise]):
    lst, flag = filter_List(data)
    # chek = createJsFgen(lst, flag)
    # print(req_math(chek))         возможность передавать уже сгенерированные задачи
    return createJsFgen(lst, flag)


def createJsFgen(lst: list[Exercise], flag: bool) -> list:
    """
    Функция, которая создаёт лист для генератора готовый для передачи в виде JSON
    :param lst: лист с задачами
    :param flag: либо положительные, либо отрицательные все задачи
    :return: лист для создания задач генератором
    """
    chek_themes = {}
    for model in lst:
        if model.theme not in chek_themes:
            chek_themes[model.theme] = model.complexity
        else:
            if flag:
                chek_themes[model.theme] = model.complexity if model.complexity > chek_themes[model.theme] \
                    else chek_themes[model.theme]
            else:
                chek_themes[model.theme] = model.complexity if model.complexity < chek_themes[model.theme] \
                    else chek_themes[model.theme]
    if flag:
        return [{
            'title': theme,
            'complexity': chek_themes[theme] + 1 if chek_themes[theme] != 2 else 2,
            'count': 1
        } for theme in chek_themes.keys()]
    else:
        return [{
            'title': theme,
            'complexity': chek_themes[theme] - 1 if chek_themes[theme] != 0 else 0,
            'count': 1
        } for theme in chek_themes.keys()]


def filter_List(lst: list[Exercise]) -> (list, bool):
    """
    :param lst: лист со всеми задачами
    :return: лист для обработки в JSON, и переменная за положительные или отрицательные задачи
    """
    negative = [mod for mod in lst if not mod.get_answer()]
    return (negative, False) if negative else (lst, True)
