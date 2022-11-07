from fuzzywuzzy import fuzz
from config import *


def select_expense_class(description: str) -> str:
    """
    Tries to find the most similar category for the expense
    :param description: description of an expense, which user adds
    :return: the enough similar category or 'another' category if such was not found
    """
    max_similarity = 75
    for category, category_triggers in expense_categories.items():
        for category_trigger in category_triggers:
            if fuzz.WRatio(category_trigger, description) >= max_similarity:
                max_similarity = fuzz.WRatio(category_trigger, description)
                result = category
    if max_similarity == 75:
        result = 'Другое'
    return result
