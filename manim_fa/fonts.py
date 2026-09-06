"""
manim_fa.fonts
==============

مدیریت فونت‌های فارسی برای پلاگین manim_fa.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import manimpango

_FONTS_DIR = Path(__file__).parent / "fonts_data"

_BUNDLED_FONTS = {
    "Vazirmatn-Regular.ttf": "Vazirmatn",
    "Vazirmatn-Bold.ttf": "Vazirmatn",
}

DEFAULT_FONT = "Vazirmatn"

KNOWN_PERSIAN_FONTS = [
    "Vazirmatn", "Vazir", "IRANSans", "Sahel", "Shabnam",
    "Noto Sans Arabic", "Noto Naskh Arabic", "IranNastaliq",
]

_fonts_registered = False


def _register_bundled_fonts() -> None:
    global _fonts_registered
    if _fonts_registered:
        return

    for filename in _BUNDLED_FONTS:
        font_path = _FONTS_DIR / filename
        if not font_path.exists():
            warnings.warn(f"[manim_fa] فایل فونت همراه پلاگین پیدا نشد: {font_path}")
            continue
        try:
            manimpango.register_font(str(font_path))
        except Exception as exc:  # noqa: BLE001
            warnings.warn(f"[manim_fa] ثبت فونت {filename} ناموفق بود: {exc}")

    _fonts_registered = True


def _font_available(font_name: str) -> bool:
    try:
        return font_name in manimpango.list_fonts()
    except Exception:  # noqa: BLE001
        return False


def resolve_font(preferred: str | None = None) -> str:
    _register_bundled_fonts()

    if preferred:
        if _font_available(preferred):
            return preferred
        warnings.warn(
            f"[manim_fa] فونت '{preferred}' پیدا نشد؛ به‌جای آن از "
            f"'{DEFAULT_FONT}' استفاده می‌شود."
        )

    for font in KNOWN_PERSIAN_FONTS:
        if _font_available(font):
            return font

    return DEFAULT_FONT


def get_persian_font(preferred: str | None = None) -> str:
    return resolve_font(preferred)
