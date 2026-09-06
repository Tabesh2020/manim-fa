# manim_fa/translit.py
# -*- coding: utf-8 -*-
"""تبدیل قاعده‌مبنای فینگلیش (لاتین) به فارسی."""

from __future__ import annotations

import re

_DIGRAPH_MAP = {
    "kh": "خ", "gh": "غ", "ch": "چ", "sh": "ش", "zh": "ژ", "th": "ث",
    "aa": "آ", "â": "آ", "ou": "او", "ow": "او", "oo": "و", "ee": "ی",
}

_SINGLE_MAP = {
    "a": "ا", "b": "ب", "p": "پ", "t": "ت", "s": "س", "j": "ج",
    "c": "ک", "k": "ک", "g": "گ", "q": "ق", "f": "ف", "v": "و",
    "w": "و", "h": "ه", "x": "خ", "y": "ی", "i": "ی", "o": "و",
    "u": "و", "r": "ر", "l": "ل", "m": "م", "n": "ن", "z": "ز",
    "d": "د", "'": "ء", "e": "",
}

_NUM_MAP = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

_DIGRAPH_PATTERN = re.compile(
    "|".join(re.escape(k) for k in sorted(_DIGRAPH_MAP, key=len, reverse=True)),
    flags=re.IGNORECASE,
)


def _replace_digraphs(text: str) -> str:
    return _DIGRAPH_PATTERN.sub(lambda m: _DIGRAPH_MAP[m.group(0).lower()], text)


def _replace_single_letters(text: str) -> str:
    return "".join(_SINGLE_MAP.get(ch.lower(), ch) for ch in text)


def _post_process_cleanup(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"آا+", "آ", text)
    text = re.sub(r"اآ+", "آ", text)
    text = re.sub(r"ا{2,}", "ا", text)
    text = re.sub(r"ء{2,}", "ء", text)
    text = re.sub(r"\s+([،؛.,!?])", r"\1", text)
    return text.strip()


def translit_to_fa(text: str, convert_numbers: bool = True) -> str:
    if not isinstance(text, str):
        return text

    if convert_numbers:
        text = text.translate(_NUM_MAP)

    tokens = re.findall(r"[A-Za-z']+|[^A-Za-z']+", text)

    out_tokens = []
    for tok in tokens:
        if re.search(r"[A-Za-z]", tok):
            t = _replace_digraphs(tok)
            t = _replace_single_letters(t)
            out_tokens.append(t)
        else:
            out_tokens.append(tok)

    return _post_process_cleanup("".join(out_tokens))
