import threading
from graph.graphDBCypher import accessGraph



async def filter_List(lst: list) -> (list, bool):
    """
    :param lst: лист со всеми задачами
    :return: лист для обработки в JSON, и переменная за положительные или отрицательные задачи
    """
    negative = [mod for mod in lst if not mod.get_answer()]
    return (negative, False) if negative else (lst, True)


async def createListJson(app, lst: list, correct: bool, list_studied=None, topic: str = '') -> dict:
    def work_foo(theme_w):
        if (chek_themes[theme_w] >= 2 and correct) or (chek_themes[theme_w] <= 0 and not correct):
            if correct:
                list_studied.append(theme_w)
            themes = accessGraph(app, theme_w, topic, correct, list_studied=list_studied)
            res.append(themes)
        else:
            if theme_w not in list_studied:
                res.append({
                    "title": theme_w,
                    'complexity': chek_themes[theme_w] + 1 if correct else chek_themes[theme_w] - 1,
                    'count': 1
                })

    if list_studied is None:
        list_studied = []
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
    threads = []
    for theme in chek_themes.keys():
        thread = threading.Thread(target=work_foo, args=(theme,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    slovar = {}

    for r in res:
        if isinstance(r, dict):
            if r['title'] in slovar:
                slovar[r['title']]['count'] += 1
            else:
                slovar[r['title']] = r
        else:
            for th in r:
                if th in slovar:
                    slovar[th]['count'] += 1
                else:
                    slovar[th] = {
                        "title": th,
                        'complexity': 0 if correct else 2,
                        'count': 1
                    }

    return {"tasks": list(slovar.values()), "studied": list(set(list_studied))}
