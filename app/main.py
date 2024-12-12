from abc import abstractmethod, ABC
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: str) -> int:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance: object, value: int) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> bool:
        if isinstance(value, int):
            if self.min_value <= value <= self.max_value:
                return True
            else:
                raise ValueError(
                    f"Quantity should not be less than {self.min_value}"
                    f" and greater than {self.max_value}."
                )
        else:
            raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self, options: tuple[str, ...]) -> None:
        self.options = options

    def validate(self, value: str) -> bool:
        if value in self.options:
            return True
        else:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
