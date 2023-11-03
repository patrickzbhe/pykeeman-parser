# Generic representation of https://www.crockford.com/mckeeman.html


class Grammar:
    def __init__(self):
        self.rules: dict[str, Rule] = {}


class Rule:
    def __init__(self, name: str, alternatives: list["Items"] = []):
        self.name = name
        self.alternatives: list[Items] = alternatives

    def __str__(self):
        return (
            f"RULE: {self.name}\n"
            + "".join([f"    {alt}\n" for alt in self.alternatives])
        )[:-1]


class Items:
    def __init__(self, items=[]):
        self.items: list[Name | Literal] = items

    def __str__(self):
        return " ".join([str(item) for item in self.items])


class Name:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Literal:
    ...


class Singleton(Literal):
    def __init__(self, codepoint: str):
        self.codepoint = codepoint

    def __str__(self):
        return self.codepoint


class RangeExclude(Literal):
    def __init__(self, start: str, end: str, exclude=None):
        self.start = start
        self.end = end
        if exclude is None:
            self.exclude = []
        else:
            self.exclude = exclude

    def __str__(self):
        return f"({self.start} - {self.end})"

    def __contains__(self, other) -> bool:
        for exclude_element in self.exclude:
            match exclude_element:
                case str():
                    if exclude_element == other:
                        return False
                case RangeExclude():
                    return other in exclude_element
                case _:
                    raise ValueError(
                        f"Checking non str or RangeExclude type ({type(exclude_element)}) in RangeExclude"
                    )
        return ord(self.start) <= ord(other) <= ord(self.end)


class Characters(Literal):
    def __init__(self, chars: str):
        self.chars = chars

    def __str__(self):
        return self.chars
