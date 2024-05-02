from typing import Optional
from pydantic import BaseModel
from graph.graphDBCypher import getThemeByIdTask, getIdByName

def get_answer(answer) -> bool:
    if isinstance(answer, bool):
        return answer
    if answer == "True":
        return True
    return False


class Theme:
    id: str
    complexity: int
    answer: bool

    def __init__(self, i: str, complexity: int = None, answer: bool= None):
        self.id = i
        self.complexity = complexity
        self.answer = answer

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id


class Base(BaseModel):
    theme: Optional[str | list[str] | None] = None
    id: Optional[str | list[str]| None] = None
    answer: str | bool
    complexity: Optional[int | None] = None

    def get_theme(self, driver):
        themes = []
        if self.complexity:
            if isinstance(self.theme, list):
                themes.extend([Theme(getIdByName(i,driver), self.complexity, get_answer(self.answer)) for i in self.theme])
            elif isinstance(self.theme, str):
                themes.append(Theme(getIdByName(self.theme, driver), self.complexity, get_answer(self.answer)))
            if isinstance(self.id, list):
                themes.extend([Theme(i,
                                     self.complexity, get_answer(self.answer)) for i in self.id])
            elif isinstance(self.id, str):
                themes.append(
                    Theme(self.id, self.complexity, get_answer(self.answer)))
        else:
            if isinstance(self.id, list):
                for i in self.id:
                    reqv = getThemeByIdTask(i, driver)
                    complexity = int(dict(reqv[0]['m'])['description'])
                    theme = [name['n']['id'] for name in reqv]
                    themes.extend([Theme(i, complexity, get_answer(self.answer)) for i in theme])
            elif isinstance(self.id, str):
                reqv = getThemeByIdTask(self.id, driver)
                complexity = int(dict(reqv[0]['m'])['description'])
                theme = [name['n']['id'] for name in reqv]
                themes.extend([Theme(i, complexity, get_answer(self.answer)) for i in theme])
        return themes

class ByReqvest(BaseModel):
    test: list[Base]
    list_studied: list[str]|None = []
    topic: str|None = None

    def get_test(self,driver):
        res = []
        for base in self.test:
            res.extend(base.get_theme(driver))
        return res






# class Exercise(BaseModel):
#     theme: Optional[str | list[str]] = None
#     id: Optional[str | list[str]] = None
#     answer: str
#     complexity: int
#
#     def get_answer(self) -> bool:
#         if isinstance(self.answer, bool):
#             return self.answer
#         if self.answer == "True":
#             return True
#         return False


# class Task(BaseModel):
#     id: str
#     answer: str | bool
#
#     def get_theme(self, app):
#         reqv = getThemeByIdTask(self.id, app)
#         complexity = dict(reqv[0]['m'])['description']
#
#         theme = [name['n']['name'] for name in reqv]
#         return Exercise(theme=theme, complexity=complexity, answer=self.answer)


# class Receipt(BaseModel):
#     test: list[Exercise] | list[Task]
#     studied: list[str] | None = None
#     topic: str | None = None
#
#     def get_test(self, app) -> list[Exercise]:
#         if isinstance(self.test[0], Task):
#             res = []
#             for i in self.test:
#                 res.append(i.get_theme(app))
#             return res
#         return self.test
#
#     def get_studied(self) -> list[str]:
#         if self.studied is None:
#             return []
#         return self.studied
