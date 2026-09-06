"""ماژول پایتون برای پردازش و نمایش متن فارسی در مانیم."""

from .text import FaText
from .fonts import resolve_font, get_persian_font
from .translit import translit_to_fa
from .markup import parse_fa_markup, has_markup
from .animation import fa_write

__version__ = "1.1.1"

__all__ = [
    "FaText",
    "resolve_font",
    "get_persian_font",
    "translit_to_fa",
    "parse_fa_markup",
    "has_markup",
    "fa_write",
]
