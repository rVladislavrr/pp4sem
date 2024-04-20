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


class Receipt(BaseModel):
    test: list[Exercise]
    studied: list[str] | None = None
    topic: str | None = None

    def get_test(self) -> list[Exercise]:
        return self.test

    def get_studied(self) -> list[str]:
        if self.studied is None:
            return []
        return self.studied
