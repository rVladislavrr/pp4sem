import sqlite3

async def findId(name_element: str, cursor) -> int:
    try:
        query = f"select themes.id from themes where themes = '{name_element}'"
        rows = cursor.execute(query)
        for row in rows:
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


