from pydantic import BaseModel


class Exercise(BaseModel):
    theme: str
    complexity: int
    answer: str | bool

    def get_answer(self) -> bool:
        if isinstance(self.answer, bool):
            return self.answer
        if self.answer == "True":
            return True
        return False
