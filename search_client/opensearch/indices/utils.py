import re
from unidecode import unidecode


def prepare_suggest_completion(*texts) -> list[str]:
    alpha_pattern = re.compile("[^a-zA-Z]+")
    return [  # removes reading signs and acutes for autocomplete suggestions
        alpha_pattern.sub("", unidecode(text))
        for text in texts
    ]
