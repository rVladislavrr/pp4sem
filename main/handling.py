import threading
from graph.graphDBCypher import accessGraph,createobj
from models.base import Theme


class MyObjForTask:
    def __init__(self, th, complexity):
        self.th = th
        self.complexity = complexity
        self.count = 2

    def __eq__(self, other):
        return self.th == other.th

    def dict(self):
        return {'title': self.th.dict(), 'complexity': self.complexity, 'count': self.count}

    def __hash__(self):
        return hash(self.th)

async def filter_List(lst: list) -> (list, bool):
    """
    :param lst: лист со всеми задачами
    :return: лист для обработки в JSON, и переменная за положительные или отрицательные задачи
    """
    negative = [mod for mod in lst if not mod.answer]
    return (negative, False) if negative else (lst, True)


async def CreateResponse(driver, lst: list[Theme], correct: bool, list_studied=None, topic: str = '') -> dict:
    def work_foo(theme_w:Theme, complexity):
        if (complexity >= 2 and correct) or (complexity <= 0 and not correct):
            if correct:
                list_studied.append(theme_w.id)
            themes = accessGraph(driver, theme_w, topic, correct, list_studied=list_studied)

            res.extend([MyObjForTask(th, 0 if correct else 2) for th in themes])
        else:
            if theme_w not in list_studied:
                obj = createobj(driver,theme_w.id)
                res.append(MyObjForTask(obj, complexity + 1 if correct else complexity - 1))

    if list_studied is None:
        list_studied = []
    chek_themes = {}

    for theme in lst:
        if theme not in chek_themes:
            chek_themes[theme] = theme.complexity
        else:
            if correct:
                chek_themes[theme] = theme.complexity if theme.complexity > chek_themes[theme] \
                    else chek_themes[theme]
            else:
                chek_themes[theme] = theme.complexity if theme.complexity < chek_themes[theme] \
                    else chek_themes[theme]
    res = []
    threads = []

    for theme in chek_themes.keys():
        thread = threading.Thread(target=work_foo, args=(theme,chek_themes[theme]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    res = list(set(res))
    res.sort(key=lambda x: x.th.description, reverse=True)
    res = res[:5]

    return {"tasks": [r.dict() for r in res], "studied": list(set(list_studied))}


# async def createListJson(app, lst: list, correct: bool, list_studied=None, topic: str = '') -> dict:
#     def work_foo(theme_w):
#         if (chek_themes[theme_w] >= 2 and correct) or (chek_themes[theme_w] <= 0 and not correct):
#             if correct:
#                 list_studied.append(theme_w)
#             themes = accessGraph(app, theme_w, topic, correct, list_studied=list_studied)
#
#             res.extend([MyObjForTask(th, 0 if correct else 2) for th in themes])
#         else:
#             if theme_w not in list_studied:
#                 obj = createobj(app, theme_w)
#
#                 res.append(MyObjForTask(obj, chek_themes[theme_w] + 1 if correct else chek_themes[theme_w] - 1))
#
#     if list_studied is None:
#         list_studied = []
#     chek_themes = {}
#     for model in lst:
#         themes_m = []
#         if model.theme:
#
#             if isinstance(model.theme, list):
#                 themes_m.extend(model.theme)
#             else:
#                 themes_m.append(model.theme)
#
#         if model.id:
#             if isinstance(model.id, list):
#                 themes_m.extend([getNameById(i, app) for i in model.id])
#
#             else:
#                 themes_m.append(getNameById(model.id, app))
#
#         for th in themes_m:
#             if th not in chek_themes:
#                 chek_themes[th] = model.complexity
#             else:
#                 if correct:
#                     chek_themes[th] = model.complexity if model.complexity > chek_themes[th] \
#                         else chek_themes[th]
#                 else:
#                     chek_themes[th] = model.complexity if model.complexity < chek_themes[th] \
#                         else chek_themes[th]
#     res = []
#     threads = []
#
#     for theme in chek_themes.keys():
#         thread = threading.Thread(target=work_foo, args=(theme,))
#         thread.start()
#         threads.append(thread)
#
#     for thread in threads:
#         thread.join()
#
#     res = list(set(res))
#     res.sort(key=lambda x: x.title.description, reverse=True)
#     res = res[:5]
#
#     return {"tasks": [r.dict() for r in res], "studied": list(set(list_studied))}
