from __future__ import unicode_literals

import glob
import inspect
import json
import re


def quote(text):
    """Returns a quoted representation of the given string, to be used
    as a C(++) string literal."""
    text = text or ""
    if not isinstance(text, basestring):
        raise TypeError("expected string")
    return json.dumps(text)


def convert_none(conversion, value):
    if value is None:
        return
    return conversion(value)


def compile_globs(patterns):
    patterns = [glob.fnmatch.translate(pattern) for pattern in patterns]
    regex = re.compile(r"\A({})\Z".format("|".join(patterns)))
    return regex


def flatten(it):
    result = []
    stack = [list(it)]
    while stack:
        if not stack[-1]:
            stack.pop()
            continue

        elem = stack[-1].pop()
        if isinstance(elem, list) or inspect.isgenerator(elem):
            stack.append(list(elem))
            continue
        result.append(elem)
    result.reverse()
    return result


def join_arguments(*arguments):
    return ", ".join([arg for arg in flatten(arguments) if arg is not None])


def strip_prefix(text, *prefixes):
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text
