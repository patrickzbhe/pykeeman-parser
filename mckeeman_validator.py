from grammar import (
    Grammar,
    Rule,
    Items,
    Singleton,
    Name,
    RangeExclude,
    Characters,
)
from validator import Validator
import sys


if __name__ == "__main__":
    mckeeman = Grammar()
    grammar = Rule("grammar", alternatives=[Items(items=[Name("rules")])])
    space = Rule("space", alternatives=[Items(items=[Singleton(" ")])])
    newline = Rule("newline", alternatives=[Items(items=[Singleton("\n")])])

    name = Rule(
        "name",
        alternatives=[
            Items(items=[Name("letter")]),
            Items(items=[Name("letter"), Name("name")]),
        ],
    )

    letter = Rule(
        "letter",
        alternatives=[
            Items(items=[RangeExclude("a", "z")]),
            Items(items=[RangeExclude("A", "Z")]),
            Items(items=[Singleton("_")]),
        ],
    )

    indentation = Rule(
        "indentation",
        alternatives=[
            Items(items=[Name("space"), Name("space"), Name("space"), Name("space")]),
        ],
    )

    rules = Rule(
        "rules",
        alternatives=[
            Items(items=[Name("rule")]),
            Items(items=[Name("rule"), Name("newline"), Name("rules")]),
        ],
    )

    rule = Rule(
        "rule",
        alternatives=[
            Items(items=[Name("name"), Name("newline"), Name("alternatives")]),
            Items(items=[Name("name"), Name("newline"), Name("nothing")]),
        ],
    )

    nothing = Rule(
        "nothing",
        alternatives=[
            Items(items=[Characters("")]),
            Items(
                items=[
                    Name("indentation"),
                    Singleton('"'),
                    Singleton('"'),
                    Name("newline"),
                ]
            ),
        ],
    )

    alternatives = Rule(
        "alternatives",
        alternatives=[
            Items(items=[Name("alternative")]),
            Items(items=[Name("alternative"), Name("alternatives")]),
        ],
    )

    alternative = Rule(
        "alternative",
        alternatives=[
            Items(
                items=[
                    Name("indentation"),
                    Name("items"),
                    Name("newline"),
                ]
            ),
        ],
    )

    items = Rule(
        "items",
        alternatives=[
            Items(items=[Name("item")]),
            Items(items=[Name("item"), Name("space"), Name("items")]),
        ],
    )

    item = Rule(
        "item",
        alternatives=[
            Items(items=[Name("literal")]),
            Items(items=[Name("name")]),
        ],
    )

    literal = Rule(
        "literal",
        alternatives=[
            Items(items=[Name("singleton")]),
            Items(items=[Name("range"), Name("exclude")]),
            Items(
                items=[
                    Singleton('"'),
                    Name("characters"),
                    Singleton('"'),
                ]
            ),
        ],
    )

    singleton = Rule(
        "singleton",
        alternatives=[
            Items(items=[Singleton("'"), Name("codepoint"), Singleton("'")]),
        ],
    )

    codepoint = Rule(
        "codepoint",
        alternatives=[
            Items(items=[RangeExclude(" ", chr(0x10FFFF))]),
            Items(items=[Name("hexcode")]),
        ],
    )

    hexcode = Rule(
        "hexcode",
        alternatives=[
            Items(
                items=[
                    Characters("10"),
                    Name("hex"),
                    Name("hex"),
                    Name("hex"),
                    Name("hex"),
                ]
            ),
            Items(
                items=[Name("hex"), Name("hex"), Name("hex"), Name("hex"), Name("hex")]
            ),
            Items(items=[Name("hex"), Name("hex"), Name("hex"), Name("hex")]),
        ],
    )

    hex = Rule(
        "hex",
        alternatives=[
            Items(items=[RangeExclude("0", "9")]),
            Items(items=[RangeExclude("A", "F")]),
        ],
    )

    range_ = Rule(
        "range",
        alternatives=[
            Items(
                items=[
                    Name("singleton"),
                    Name("space"),
                    Singleton("."),
                    Name("space"),
                    Name("singleton"),
                ]
            ),
        ],
    )

    exclude = Rule(
        "exclude",
        alternatives=[
            Items(items=[Characters("")]),
            Items(
                items=[
                    Name("space"),
                    Singleton("-"),
                    Name("space"),
                    Name("singleton"),
                    Name("exclude"),
                ]
            ),
            Items(
                items=[
                    Name("space"),
                    Singleton("-"),
                    Name("space"),
                    Name("range"),
                    Name("exclude"),
                ]
            ),
        ],
    )

    characters = Rule(
        "characters",
        alternatives=[
            Items(items=[Name("character")]),
            Items(items=[Name("character"), Name("characters")]),
        ],
    )

    character = Rule(
        "character",
        alternatives=[
            Items(items=[RangeExclude(" ", chr(0x10FFFF), [Singleton('"')])]),
        ],
    )

    mckeeman.rules = {
        "grammar": grammar,
        "space": space,
        "newline": newline,
        "name": name,
        "letter": letter,
        "indentation": indentation,
        "rules": rules,
        "rule": rule,
        "nothing": nothing,
        "alternatives": alternatives,
        "alternative": alternative,
        "items": items,
        "item": item,
        "literal": literal,
        "singleton": singleton,
        "codepoint": codepoint,
        "hexcode": hexcode,
        "hex": hex,
        "range": range_,
        "exclude": exclude,
        "characters": characters,
        "character": character,
    }

    with open(sys.argv[1], "r") as f:
        input_str = f.read()
        mckeeman_validator = Validator(input_str, mckeeman)
        print(mckeeman_validator.validate())
