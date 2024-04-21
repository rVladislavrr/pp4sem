from graph.graphDBCypher import accessGraph

async def filter_List(lst: list) -> (list, bool):
    """
    :param lst: лист со всеми задачами
    :return: лист для обработки в JSON, и переменная за положительные или отрицательные задачи
    """
    negative = [mod for mod in lst if not mod.get_answer()]
    return (negative, False) if negative else (lst, True)

async def createListJson(app, lst: list, correct: bool, list_studied=None, topic: str = '') -> dict:
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
    awRes = []

    for theme in chek_themes.keys():
        if (chek_themes[theme] >= 2 and correct) or (chek_themes[theme] <= 0 and not correct):
            if correct:
                list_studied.append(theme)
            r = accessGraph(app, theme, topic, correct, list_studied=list_studied)
            awRes.append(r)
        else:
            res.append({
                'title': theme,
                'complexity': chek_themes[theme] + 1 if correct else chek_themes[theme] - 1,
                'count': 1
            })

    for r in awRes:
        for rr in await r:
            res.append(rr)

    new_obj = {}

    for obj in res:
        if obj['title'] not in list_studied:
            if obj['title'] in new_obj:
                new_obj[obj['title']]['count'] += 1
            else:
                new_obj[obj['title']] = obj

    return {"tasks": list(new_obj.values()), "studied": list(set(list_studied))}
