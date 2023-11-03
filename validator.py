from grammar import (
    Grammar,
    Rule,
    Items,
    Literal,
    Singleton,
    Name,
    RangeExclude,
    Characters,
)


class Validator:
    """Backtrack every possibility until one matches entire input string"""

    def __init__(self, input_str: str, grammar: Grammar):
        self.input_str = input_str
        self.grammar = grammar
        self.pos = 0

    def pos_check_overflow(self):
        if self.pos > len(self.input_str):
            return True
        return False

    def validate(self) -> bool:
        return self.validate_grammar(self.grammar)

    def validate_grammar(self, grammar: Grammar):
        if not grammar.rules:
            return
        entry_rule = list(grammar.rules.values())[0]
        self.pos = 0
        gen = self.validate_rule(entry_rule)
        while True:
            try:
                next(gen)
                if self.pos == len(self.input_str):
                    return True
            except StopIteration:
                return False

    def validate_rule(self, rule: Rule):
        old_pos = self.pos
        for alternative in rule.alternatives:
            yield from self.validate_items(alternative)
            self.pos = old_pos

    def get_gen(self, item: Name | Literal):
        match item:
            case Name():
                gen = self.validate_name
            case Singleton():
                gen = self.validate_singleton
            case RangeExclude():
                gen = self.validate_range_exclude
            case Characters():
                gen = self.validate_characters
            case _:
                raise Exception("Unexpected item; Invalid grammar")
        return gen

    def validate_items(self, items: Items):
        def validate_items_inner(items: list[Name | Literal]):
            if not items:
                yield
                return
            old_pos = self.pos
            total = 0
            gen = self.get_gen(items[0])
            temp = gen(items[0])

            while True:
                try:
                    next(temp)
                except StopIteration:
                    break
                total += 1
            for i in range(1, total + 1):
                self.pos = old_pos
                temp = gen(items[0])
                for _ in range(i):
                    next(temp)
                yield from validate_items_inner(items[1:])

        yield from validate_items_inner(items.items)

    def validate_name(self, name: Name):
        if name.name not in self.grammar.rules:
            raise Exception("Invalid grammar")
        else:
            yield from self.validate_rule(self.grammar.rules[name.name])

    def validate_singleton(self, singleton: Singleton):
        if not self.input_str[self.pos :].startswith(singleton.codepoint):
            return
        self.pos += 1
        if self.pos_check_overflow():
            return
        yield

    def validate_range_exclude(self, range_exclude: RangeExclude):
        if (
            self.pos >= len(self.input_str)
            or self.input_str[self.pos] not in range_exclude
        ):
            return
        self.pos += 1
        if self.pos_check_overflow():
            return
        yield

    def validate_characters(self, characters: Characters):
        if not self.input_str[self.pos :].startswith(characters.chars):
            return
        self.pos += len(characters.chars)
        if self.pos_check_overflow():
            return
        yield
