from models.base import Exercise
from graph.accessDB import *


async def changeTheme(theme: str, dirOfChange: bool = False) -> list[dict]:
    themes = findElements(theme, dirOfChange)
    return [{
        "title": th,
        "count": 1,
        "complexity": 0 if dirOfChange else 2
    } for th in await themes]


async def createJsFgen(lst: list[Exercise], correct: bool) -> list:
    """
    Функция, которая создаёт лист для генератора готовый для передачи в виде JSON
    :param lst: лист с задачами
    :param correct: либо положительные, либо отрицательные все задачи
    :return: лист для создания задач генератором
    """
    chek_themes = {}
    for model in lst:
        if model.theme not in chek_themes:
            chek_themes[model.theme] = model.complexity
        else:
            if correct:
                chek_themes[model.theme] = model.complexity if model.complexity > chek_themes[model.theme] \
                    else chek_themes[model.theme]
            else:
                chek_themes[model.theme] = model.complexity if model.complexity < chek_themes[model.theme] \
                    else chek_themes[model.theme]
    res = []
    for theme in chek_themes.keys():
        if (chek_themes[theme] >= 2 and correct) or (chek_themes[theme] <= 0 and not correct):
            res += await changeTheme(theme, correct)
        else:
            res.append({
                'title': theme,
                'complexity': chek_themes[theme] + 1 if correct else chek_themes[theme] - 1,
                'count': 1
            })
    new_obj = {}
    print(res)
    for obj in res:
        if obj['title'] in new_obj:
            new_obj[obj['title']]['count'] += 1
        else:
            new_obj[obj['title']] = obj
    return list(new_obj.values())



async def filter_List(lst: list[Exercise]) -> (list, bool):
    """
    :param lst: лист со всеми задачами
    :return: лист для обработки в JSON, и переменная за положительные или отрицательные задачи
    """
    negative = [mod for mod in lst if not mod.get_answer()]
    return (negative, False) if negative else (lst, True)
