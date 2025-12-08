from enum import Enum


class FoodType(str, Enum):
    BREAKFAST = "BREAKFAST"
    DESSERT = "DESSERT"
    DINNER = "DINNER"
    DRINK = "DRINK"
    LUNCH = "LUNCH"
    SNACK = "SNACK"

    def __str__(self) -> str:
        return str(self.value)
