"""
manim_fa.markup
================

تبدیل یک نحوِ ساده و آشنا (شبیه مارک‌داون) به Pango Markup، تا کاربر
بدون دانستن Pango Markup یا اندیس کاراکترها بتواند بخشی از متن را
بولد/ایتالیک/زیرخط‌دار/هایلایت کند.

نحو پشتیبانی‌شده:
    **متن**       -> بولد
    *متن*         -> ایتالیک (کج)
    __متن__       -> زیرخط‌دار (Underline)
    ==متن==       -> هایلایت با رنگ پیش‌فرض
    ==متن|رنگ==   -> هایلایت با رنگ دلخواه، مثل ==نکته‌ی مهم|orange==

برای نوشتن خودِ نویسه‌های ویژه («*»، «_»، «=») به‌صورت عادی (بدون این‌که
به‌عنوان علامتِ قالب‌بندی خوانده شوند)، قبلشان یک بک‌اسلش بگذارید:
``\\*``, ``\\_``, ``\\=``.
"""

from __future__ import annotations

import html
import re

DEFAULT_HIGHLIGHT_COLOR = "yellow"
DEFAULT_HIGHLIGHT_TEXT_COLOR = "black"

# ترتیب مهم است: هایلایت و بولد باید قبل از ایتالیک بررسی شوند وگرنه
# "**" به اشتباه به دو "*" ایتالیکِ تو‌در‌تو تفسیر می‌شود.
_TAG_PATTERN = re.compile(
    r"(?<!\\)==(?P<hltext>[^=|]+)\|(?P<hlcolor>[A-Za-z_][A-Za-z0-9_]*)(?<!\\)=="
    r"|(?<!\\)==(?P<highlight>[^=|]+)(?<!\\)=="
    r"|(?<!\\)\*\*(?P<bold>[^*]+)(?<!\\)\*\*"
    r"|(?<!\\)__(?P<underline>[^_]+)(?<!\\)__"
    r"|(?<!\\)\*(?P<italic>[^*]+)(?<!\\)\*",
    re.DOTALL,
)

_ESCAPES = {r"\*": "*", r"\_": "_", r"\=": "="}
_UNESCAPE_PATTERN = re.compile("|".join(re.escape(k) for k in _ESCAPES))


def _unescape(text: str) -> str:
    return _UNESCAPE_PATTERN.sub(lambda m: _ESCAPES[m.group(0)], text)


def used_highlight_colors(text: str, highlight_color: str = DEFAULT_HIGHLIGHT_COLOR) -> set[str]:
    """مجموعه‌ی رنگ‌های پس‌زمینه‌ای که در ==...== یا ==...|رنگ== این متن
    استفاده شده‌اند را برمی‌گرداند (برای استفاده‌ی داخلیِ ``fa_write``)."""
    colors: set[str] = set()
    for m in _TAG_PATTERN.finditer(text):
        if m.group("hltext") is not None:
            colors.add(m.group("hlcolor"))
        elif m.group("highlight") is not None:
            colors.add(highlight_color)
    return colors


def has_markup(text: str) -> bool:
    """آیا این متن حاوی یکی از نشانه‌های قالب‌بندیِ ما هست؟"""
    return bool(_TAG_PATTERN.search(text))


def parse_fa_markup(text: str, highlight_color: str = DEFAULT_HIGHLIGHT_COLOR) -> str:
    """متن با نحوِ ساده‌ی بالا را به یک رشته‌ی معتبرِ Pango Markup تبدیل می‌کند."""
    out: list[str] = []
    pos = 0
    for m in _TAG_PATTERN.finditer(text):
        out.append(html.escape(_unescape(text[pos : m.start()]), quote=False))

        if m.group("hltext") is not None:
            inner = html.escape(_unescape(m.group("hltext")), quote=False)
            color = m.group("hlcolor")
            out.append(
                f'<span background="{color}" foreground="{DEFAULT_HIGHLIGHT_TEXT_COLOR}">{inner}</span>'
            )
        elif m.group("highlight") is not None:
            inner = html.escape(_unescape(m.group("highlight")), quote=False)
            out.append(
                f'<span background="{highlight_color}" foreground="{DEFAULT_HIGHLIGHT_TEXT_COLOR}">{inner}</span>'
            )
        elif m.group("bold") is not None:
            inner = html.escape(_unescape(m.group("bold")), quote=False)
            out.append(f"<b>{inner}</b>")
        elif m.group("underline") is not None:
            inner = html.escape(_unescape(m.group("underline")), quote=False)
            out.append(f"<u>{inner}</u>")
        elif m.group("italic") is not None:
            inner = html.escape(_unescape(m.group("italic")), quote=False)
            out.append(f"<i>{inner}</i>")

        pos = m.end()

    out.append(html.escape(_unescape(text[pos:]), quote=False))
    return "".join(out)
