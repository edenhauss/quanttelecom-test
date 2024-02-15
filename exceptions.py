class ExpressionInputError(BaseException):
    def __init__(self) -> None:
        super().__init__("Неверно задано выражение")

class PriorityInputError(ValueError):
    def __init__(self) -> None:
        super().__init__("Неверно задан приоритет очереди")