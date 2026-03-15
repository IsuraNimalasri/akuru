"""Question builders for the 10-level path."""

from dataclasses import dataclass
import random
from typing import List

from .constants import OBJECT_TYPES, QUESTIONS_PER_LEVEL


@dataclass
class Question:
    level: int
    prompt: str
    correct: int
    choices: List[int]
    operator: str = ""
    left: int = 0
    right: int = 0
    object_type: str = "balls"
    show_pictures: bool = True


def _choice_set(answer: int, minimum: int, maximum: int, count: int, rng: random.Random) -> List[int]:
    options = {answer}
    while len(options) < count:
        options.add(rng.randint(minimum, maximum))
    result = list(options)
    rng.shuffle(result)
    return result


def _pick_object(rng: random.Random) -> str:
    return rng.choice(OBJECT_TYPES)


def generate_level_questions(level: int, rng: random.Random | None = None) -> List[Question]:
    randomizer = rng or random.Random()
    questions: List[Question] = []

    for _ in range(QUESTIONS_PER_LEVEL):
        obj = _pick_object(randomizer)

        if level == 1:
            value = randomizer.randint(1, 5)
            questions.append(
                Question(
                    level=level,
                    prompt="?",
                    correct=value,
                    choices=_choice_set(value, 1, 5, 3, randomizer),
                    object_type=obj,
                    left=value,
                )
            )
            continue

        if level == 2:
            value = randomizer.randint(1, 10)
            questions.append(
                Question(
                    level=level,
                    prompt="?",
                    correct=value,
                    choices=_choice_set(value, 1, 10, 3, randomizer),
                    object_type=obj,
                    left=value,
                )
            )
            continue

        if level == 3:
            value = randomizer.randint(1, 10)
            questions.append(
                Question(
                    level=level,
                    prompt="=",
                    correct=value,
                    choices=_choice_set(value, 1, 10, 3, randomizer),
                    object_type=obj,
                    left=value,
                )
            )
            continue

        if level == 4:
            a = randomizer.randint(1, 4)
            b = randomizer.randint(1, 5 - a)
            total = a + b
            questions.append(
                Question(
                    level=level,
                    prompt="+",
                    correct=total,
                    choices=_choice_set(total, 1, 5, 3, randomizer),
                    operator="+",
                    left=a,
                    right=b,
                    object_type=obj,
                )
            )
            continue

        if level == 5:
            a = randomizer.randint(1, 7)
            b = randomizer.randint(1, 10 - a)
            total = a + b
            questions.append(
                Question(
                    level=level,
                    prompt="+",
                    correct=total,
                    choices=_choice_set(total, 1, 10, 3, randomizer),
                    operator="+",
                    left=a,
                    right=b,
                    object_type=obj,
                )
            )
            continue

        if level == 6:
            a = randomizer.randint(2, 5)
            b = randomizer.randint(1, a - 1)
            total = a - b
            questions.append(
                Question(
                    level=level,
                    prompt="-",
                    correct=total,
                    choices=_choice_set(total, 0, 5, 3, randomizer),
                    operator="-",
                    left=a,
                    right=b,
                    object_type=obj,
                )
            )
            continue

        if level == 7:
            a = randomizer.randint(2, 10)
            b = randomizer.randint(1, a - 1)
            total = a - b
            questions.append(
                Question(
                    level=level,
                    prompt="-",
                    correct=total,
                    choices=_choice_set(total, 0, 10, 3, randomizer),
                    operator="-",
                    left=a,
                    right=b,
                    object_type=obj,
                )
            )
            continue

        if level == 8:
            op = randomizer.choice(["+", "-"])
            if op == "+":
                a = randomizer.randint(1, 7)
                b = randomizer.randint(1, 10 - a)
                total = a + b
            else:
                a = randomizer.randint(2, 10)
                b = randomizer.randint(1, a - 1)
                total = a - b

            questions.append(
                Question(
                    level=level,
                    prompt=op,
                    correct=total,
                    choices=_choice_set(total, 0, 10, 3, randomizer),
                    operator=op,
                    left=a,
                    right=b,
                    object_type=obj,
                )
            )
            continue

        if level == 9:
            op = randomizer.choice(["+", "-"])
            if op == "+":
                a = randomizer.randint(1, 9)
                b = randomizer.randint(1, 10 - a)
                total = a + b
            else:
                a = randomizer.randint(2, 10)
                b = randomizer.randint(1, a - 1)
                total = a - b
            questions.append(
                Question(
                    level=level,
                    prompt=f"{a} {op} {b}",
                    correct=total,
                    choices=_choice_set(total, 0, 10, 3, randomizer),
                    operator=op,
                    left=a,
                    right=b,
                    object_type=obj,
                    show_pictures=False,
                )
            )
            continue

        # level 10: soft challenge
        op = randomizer.choice(["+", "-"])
        if op == "+":
            a = randomizer.randint(1, 9)
            b = randomizer.randint(1, 12 - a)
            total = a + b
        else:
            a = randomizer.randint(3, 12)
            b = randomizer.randint(1, a - 1)
            total = a - b
        questions.append(
            Question(
                level=level,
                prompt=f"{a} {op} {b}",
                correct=total,
                choices=_choice_set(total, 0, 12, 3, randomizer),
                operator=op,
                left=a,
                right=b,
                object_type=obj,
                show_pictures=randomizer.choice([True, False]),
            )
        )

    return questions
