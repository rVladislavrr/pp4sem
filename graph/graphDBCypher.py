class GraphObject:
    def __init__(self, obj):
        obj = dict(obj)
        self.id = obj['id']
        self.description = obj['description']

    def dict(self):
        return self.id

    def __lt__(self, other):
        return self.description < other.description


def behindFoo(driver, id_n):
    with driver.session() as session:
        query = """MATCH (n:theme)-[:uses]->(:theme{id: $id}) RETURN n"""
        res = list(session.run(query, id=id_n))
        if res:
            result = [GraphObject(i['n']) for i in res]
            return list(set(result))
        return []


def nextFoo(driver, id_m: str):
    with driver.session() as session:
        query = """MATCH (:theme{id: $id})-[:uses]->(n:theme) RETURN n"""

        res = list(session.run(query, id=id_m))
        if res:
            result = [GraphObject(i['n']) for i in res]
            return list(set(result))
        return []


def pathFoo(driver, start: str, end: str):
    if start == end:
        return nextFoo(driver, start)[:1]
    with driver.session() as session:
        query = """MATCH path = shortestPath((start:theme {id: $name1})-[*]->(end:theme{id: $name2})) RETURN path"""
        res = list(session.run(query, name1=start, name2=end))
        if res:
            r = res[0]['path']
            return [GraphObject(i) for i in r.nodes]
        return []


def accessGraph(app, theme, topic=None, correct=False, list_studied=None):
    if correct:
        return [i for i in pathFoo(app, theme.id, topic)
                if i.id not in list_studied] if topic else [i for i in nextFoo(app, theme.id)
                                                            if i.id not in list_studied]
    else:
        return [i for i in behindFoo(app, theme.id) if i.id not in list_studied]


def createobj(app, id_w):
    with app.session() as session:
        query = """MATCH (n:theme{id: $name2})RETURN n"""
        res = list(session.run(query, name2=id_w))
        if res:
            result = [GraphObject(i['n']) for i in res]
            return result[0]
        return []


def getThemeByIdTask(id_task, app):
    with app.session() as session:
        query = """MATCH (n:theme)-[:uses]->(m:task{id: $id}) RETURN n,m"""
        res = list(session.run(query, id=id_task))
        if res:
            return res
        return []


def getIdByName(name, app):
    with app.session() as session:
        query = """MATCH (n:theme{name: $name}) RETURN n"""
        res = list(session.run(query, name=name))
        if res:
            for i in res:
                return dict(i['n'])['id']
        return ''
