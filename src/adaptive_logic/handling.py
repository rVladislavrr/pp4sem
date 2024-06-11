from src.graph.graphDBCypher import (
    createobj,
    GraphTheme,
    behindFoo,
    pathFoo,
    nextFoo,
    get_name_id_graph,
    get_id_name_graph,
    get_all_task)
from src.adaptive_logic.schemes import ThemeReq


async def get_list_res_neg(neg_list):
    res = []
    foundMinCompl = {}
    for mod in neg_list:
        if mod.id in foundMinCompl:
            if mod.complexity < foundMinCompl[mod.id]:
                foundMinCompl[mod.id] = mod.complexity
        else:
            foundMinCompl[mod.id] = mod.complexity

    for id_name, complexity in foundMinCompl.items():
        if 0 < complexity:
            obj = createobj(id_name)
            if not obj:
                continue
            obj.count = 1
            obj.complexity = complexity - 1
            res.append(obj)
        else:
            list_obj = behindFoo(id_name)
            for obj in list_obj:
                obj.count = 1
                obj.complexity = 2
            res.extend(list_obj)
    return res


async def get_list_res_pos(pos_list, topic: str, list_studied=[]):
    res = []
    foundMinCompl = {}

    for mod in pos_list:
        if mod.id in foundMinCompl:
            if mod.complexity > foundMinCompl[mod.id]:
                foundMinCompl[mod.id] = mod.complexity
        else:
            foundMinCompl[mod.id] = mod.complexity
    for id_name, complexity in foundMinCompl.items():
        if 1 < complexity:
            if createobj(id_name):
                list_studied.append(id_name)
            if topic:
                list_obj = pathFoo(id_name, topic, list_studied)
            else:
                list_obj = nextFoo(id_name)
            for obj in list_obj:
                obj.count = 1
                obj.complexity = 0
            res.extend(list_obj)
        else:
            obj = createobj(id_name)
            if not obj:
                continue
            obj.count = 1
            obj.complexity = complexity + 1
            res.append(obj)
    return res


async def create_with_neg(neg_list: list[ThemeReq], pos_list: list, count: int, list_studied: list,
                          topic: str = ''):
    res = await get_list_res_neg(neg_list)
    res = list(set(res))
    if len(res) > count:
        res.sort(key=lambda x: x.description, reverse=True)
        res: list[GraphTheme] = res[:count]
        return res, list_studied
    else:
        res_pos = await get_list_res_pos(pos_list, topic, list_studied)
        res_pos = list(set(res_pos))
        res_pos.sort(key=lambda x: x.description, reverse=True)
        res = res + res_pos[:count - len(res)]
        if len(res) < count:
            n = len(res)
            for r in res:
                r.count += 1
                n += 1
                if n >= count:
                    break
        return res, list_studied


async def create_positive(pos_list: list[ThemeReq], count: int, list_studied: list, topic: str = ''):
    res = await get_list_res_pos(pos_list, topic, list_studied)
    res = list(set(res))
    res = [theme for theme in res if theme.id not in list_studied]
    if len(res) > count:
        res.sort(key=lambda x: x.description, reverse=True)
        res: list[GraphTheme] = res[:count]
        return res, list_studied
    else:
        if len(res) < count:
            n = len(res)
            for r in res:
                r.count += 1
                n += 1
                if n >= count:
                    break
        return res, list_studied


async def create_res(data, bool_answer=False):
    test, count = data.get_test()
    if bool_answer:
        count = 999
    negative = [mod for mod in test if not mod.answer]
    positive = [mod for mod in test if mod.answer]
    if negative:
        return await create_with_neg(negative, positive, count, data.list_studied, data.topic)
    return await create_positive(positive, count, data.list_studied, data.topic)


def get_name_id(id_name):
    return get_name_id_graph(id_name)


def get_id_name(name):
    return get_id_name_graph(name)


def get_best_task(list_theme, all_task):
    best_count = 0
    best_task = None
    for task in all_task:
        matching_theme = set(task.get('related_themes')) & set(list_theme)
        if len(matching_theme) > best_count:
            best_count = len(matching_theme)
            best_task = task
    if best_task:
        return best_task
    return []


def create_task(res: list[GraphTheme]):
    res = [inx.id for inx in res]
    answer_list = []
    all_task = get_all_task()
    while res:
        best_task = get_best_task(res, all_task)
        if best_task:
            answer_list.append({'id': best_task.get('task_name')})
            res = [theme for theme in res if theme not in best_task.get('related_themes')]
        else:
            break
    return answer_list
