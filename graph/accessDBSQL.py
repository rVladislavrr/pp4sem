import sqlite3
from graph.graphDBCypher import GraphObject
# def SqlCreater(driver):
#     conn = sqlite3.connect('graph.db')
#     with driver.session() as session:
#         query = """MATCH (n) RETURN n"""
#         res = list(map(lambda x: GraphObject(x['n']), session.run(query)))
#         res.sort()
#         for i in res:
#             print(i)
#     pass

async def findId(name_element: str, cursor) -> int:
    try:
        query = f"select themes.id from themes where themes = '{name_element}'"
        row = cursor.execute(query).fetchone()
        return row[0]
    except Exception as e:
        return -1

async def findElements(name_element: str, direction: bool = False) -> list:
    try:
        conn = sqlite3.connect('graph.db')
        cursor = conn.cursor()
        id_element = findId(name_element,cursor)
        query = f"""select themes.themes 
                        from links join themes
                        on {"links.'to' = themes.id" if direction else "links.'from'= themes.id"}
                         where {f"links.'from' = {await id_element}" if direction else f"links.'to' = {await id_element}"}
                """
        rows = cursor.execute(query)
        res = []
        for row in rows:
            res.append(row[0])
        conn.close()
        return res
    except Exception as e:
        return [-1]
# {'Опр. Определителя (через подстановки)': 2, 'Св-во Сложения матриц (коммутативность)': 2, 'Опр. Невырожденной матрицы': 2, 'Св-во Произведения матрицы на число (на единицу)': 2, 'Св-во Обращения матрицы (обратная к обратной)': 2, 'Св-во Обращения матрицы (от произведения)': 2, 'Матрица': 2, 'Опр. Вырожденной матрицы': 1, 'Опр. Матричного уравнения': 2}

