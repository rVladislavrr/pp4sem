from fastapi.testclient import TestClient
async def accessGraph(app , theme: str, topic, correct: bool = False, list_studied: list = []) -> list:
    client = TestClient(app)
    if correct:
        if topic:
            response = client.get(f"/path/{theme}/{topic}").json()
            if len(response) > 1:
                res = [{"title": response[i], "count": 1, "complexity": 0} for i in range(1, len(response))]
                for r in res:
                    if r["title"] not in list_studied:
                        return [r]
        else:
            response = client.get(f"/next/{theme}").json()
            return [{"title": node, "count": 1, "complexity": 0} for node in response]
    else:
        response = client.get(f"/behind/{theme}").json()
        return [{"title": node, "count": 1, "complexity": 0} for node in response]
    return []