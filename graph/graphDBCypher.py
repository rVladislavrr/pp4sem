
def behindFoo(driver,name_theme):
    with driver.session() as session:
        query = """MATCH (n:theme)-[:uses]->(:theme{name: $name2}) RETURN n"""
        res = list(session.run(query, name2=name_theme))
        if res:
            result = [dict(i['n'])['name'] for i in res]
            return list(set(result))
        return []

def nextFoo(driver, name_theme: str):
    with driver.session() as session:
        query = """MATCH (:theme{name: $name2})-[:uses]->(n:theme) RETURN n"""
        res = list(session.run(query, name2=name_theme))
        if res:
            result = [dict(i['n'])['name'] for i in res]
            return list(set(result))
        return []


def pathFoo(driver, start: str, end: str):
    with driver.session() as session:
        query = """MATCH path = shortestPath((start:theme {name: $name1})-[*]->(end:theme{name: $name2})) RETURN path"""
        res = list(session.run(query, name1=start, name2=end))
        if res:
            r = res[0]['path']
            return [dict(i)['name'] for i in r.nodes]
        return []

def accessGraph(app, theme, topic=None, correct=False, list_studied=None):
    if correct:
        return [i for i in pathFoo(app, theme, topic) if i not in list_studied] if topic else [i for i in nextFoo(app, theme) if i not in list_studied]
    else:
        return [i for i in behindFoo(app, theme) if i not in list_studied]




