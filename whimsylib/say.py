import random
import re
import textwrap
from shutil import get_terminal_size

from whimsylib.zalgo import Zalgo
from whimsylib.globals import G


_Z = Zalgo()
_Z.numAccentsUp = (1, 10)
_Z.numAccentsDown = (1, 10)
_Z.numAccentsMiddle = (1, 4)


_VOICES = [
    "HEEEHEHEHEHEHE",
    "THERE IS NO HOPE",
    "DID YOU HEAR THAT?",
    "I PROMISE YOU KNOWLEDGE",
]


def _y(x):
    """Shallow parabolic curve ensuring zalgo increases little at first.

    Then explodes.
    """
    return (5 / 900) * (x**2) + (4 / 9) * x


def _hear_voices(text: str, insanity: int) -> str:
    # TODO: Too much zalgo text! Decide letter-by-letter whether to zalgofy.
    _Z.zalgoChance = _y(insanity) / 100
    _Z.maxAccentsPerLetter = max(1, int(insanity / 10))

    # TODO: Condition number of breakpoints on length of text!
    num_breaks = int((insanity - 40) / 10)
    breakpoints = []
    if num_breaks > 0:
        breaks = [0]
        breaks.extend(
            sorted(random.sample(range(len(text)), min(num_breaks, len(text))))
        )
        breaks.append(len(text))
        breakpoints.extend(zip(breaks[:-1], breaks[1:]))
    else:
        breakpoints.append((0, len(text)))

    segments = []
    for i, (begin, end) in enumerate(breakpoints):
        if i > 0:
            segments.append(random.choice(_VOICES))
        segments.append(_Z.zalgofy(text[begin:end]))

    return "".join(segments)


def output(msg: str) -> None:
    """Print a message.

    Unlike print(), this deals with de-denting and wrapping of text to fit
    within the width of the terminal.

    Paragraphs separated by blank lines in the input will be wrapped
    separately.
    """
    msg = re.sub(r"^[ \t]*(.*?)[ \t]*$", r"\1", msg, flags=re.M)
    paragraphs = re.split(r"\n(?:[ \t]*\n)", msg)
    formatted = [
        textwrap.fill(p.strip(), width=get_terminal_size()[0]) for p in paragraphs
    ]
    print("\n\n".join(formatted))


def insayne(text: str, add_newline=True, insanity=None) -> None:
    """Renders @text to screen, modified based on player's insanity stat.

    Interpolates arcane markings and violent exhortations if player's sanity
    is not pristine. Renders UI text less and less legible as sanity degrades.
    """
    if add_newline:
        output("")
    if insanity is None:
        insanity = G.player.insanity.value
    text = _hear_voices(text, insanity)
    output(text)


def capitalized(text: str) -> str:
    """Naively capitalizes the first character in some text.

    TODO: Make this function smarter, e.g. when text starts with non-ASCII.
    """
    return text[0].upper() + text[1:]


def a(text: str) -> str:
    """Naively generates the correct form of the indefinite article."""
    if re.search(r"^[aeiou]", text):
        return f"an {text}"
    return f"a {text}"
