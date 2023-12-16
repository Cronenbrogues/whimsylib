import functools
import logging
import inspect
import re

from whimsylib import say
from whimsylib.globals import poll_events


class _InvalidCommand(Exception):
    pass


class _CommandTemplate:
    _FORMULA_PATTERN = re.compile("^[a-z][a-z0-9_]*$")
    _ARGUMENT_PATTERN = re.compile("^[A-Z][A-Z0-9_]*$")

    def __init__(self, command_template, context=None):
        match = []
        self._prefix = None
        self._arguments = []
        self._command_template = command_template

        # TODO: Do we need the prefixes?
        for i, word in enumerate(command_template.strip().split()):
            logging.debug("word IS %s", word)
            if self._FORMULA_PATTERN.search(word):
                match.append(r"" + word)
            elif self._ARGUMENT_PATTERN.search(word):
                if i == 0:
                    raise _InvalidCommand("Commands must start with a minuscule word.")
                # Prefix consists of all non-argument terms before first argument.
                if self._prefix is None:
                    self._prefix = " ".join(match)
                word = word.lower()
                self._arguments.append(word)
                match.append(r"" + f"(?P<{word}>.*)")
            else:
                raise _InvalidCommand(
                    "All words in a command must start with a letter and "
                    "consist only of letters and numbers. Letters in each "
                    "word must all be of the same case."
                )
        self._pattern = re.compile(r"^" + r" +".join(match) + r"$", re.IGNORECASE)
        logging.debug(self._pattern)

    @property
    def command_template(self):
        return self._command_template

    @property
    def arguments(self):
        return self._arguments

    @property
    def prefix(self):
        return self._prefix

    def match(self, command):
        return self._pattern.match(command)


class CommandHandler:
    COMMANDS = []

    @classmethod
    def register(cls, command, function, context=None, **kwargs):
        command_template = _CommandTemplate(command, context)

        signature = inspect.signature(function)
        base_args = {arg: "dummy" for arg in command_template.arguments}
        base_args.update(kwargs)
        try:
            _ = signature.bind(**base_args)
        except TypeError:
            raise _InvalidCommand(
                f"Function with signature {signature} cannot accept arguments/keyword arguments "
                f"{base_args}."
            )

        cls.COMMANDS.append((command_template, function, kwargs))

    @classmethod
    def handle(cls, command):
        command = command.lower().strip()
        max_matches = -1
        call_me = None
        func_me = None
        for template, function, kwargs in cls.COMMANDS:
            match = template.match(command)
            if match is not None:
                call_kwargs = match.groupdict()
                if len(call_kwargs) > max_matches:
                    max_matches = len(call_kwargs)
                    call_kwargs.update(kwargs)
                    call_me = call_kwargs
                    func_me = function
        if func_me is not None:
            func_me(**call_me)
        else:
            say.insayne(f'I don\'t understand "{command}."')


def handle(command):
    CommandHandler.handle(command)


def poll(poll_before=True, poll_after=True):
    def poll_decorator(function):
        @functools.wraps(function)
        def poll_wrapped(*args, **kwargs):
            with poll_events(poll_before, poll_after):
                return function(*args, **kwargs)

        return poll_wrapped

    return poll_decorator


def when(command, context=None, **kwargs):
    """Decorator for command functions."""

    def when_wrapped(function):
        CommandHandler.register(command, function, context, **kwargs)
        return function

    return when_wrapped


# `help` should be available unconditionally.
@when("help")
def _help():
    """Prints this help message."""
    # TODO: Sort.
    for command, function, _ in CommandHandler.COMMANDS:
        hint = f"{command.command_template}"
        docstring = function.__doc__
        if docstring:
            first_line = docstring.split("\n")[0]
            hint += f": {first_line}"
        say.insayne(hint)


# `exit` and `quit` should be available unconditionally.
@when("exit")
@when("quit")
def _exit():
    raise KeyboardInterrupt
