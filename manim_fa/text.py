"""
manim_fa.text
=============

FaText: نمایش صحیح متن فارسی/عربی در مانیم، با پشتیبانی از قالب‌بندیِ
درون‌خطی ساده (بولد، ایتالیک، زیرخط، هایلایت).

نکات فنی:
- راست‌چین شدن و اتصال صحیح حروف را خود Pango (موتور متنِ مانیم) انجام
  می‌دهد؛ هیچ پردازش دستی (reshape/bidi) روی متن اعمال نمی‌شود، چون این
  کار با آزمایش عینی (OCR + بازرسی چشمی رندر واقعی) خرابکار تشخیص داده
  شد.
- برای قالب‌بندیِ درون‌خطی (بولد/ایتالیک/زیرخط/هایلایت) از موتور
  ``MarkupText`` مانیم استفاده می‌شود که خودش بر پایه‌ی Pango Markup
  است و با متن فارسی هم به‌درستی کار می‌کند (با رندر واقعی و بازرسی
  چشمی تأیید شد).
"""

from __future__ import annotations

from functools import lru_cache

from manim import MarkupText, VGroup

from .fonts import resolve_font
from .markup import (
    DEFAULT_HIGHLIGHT_COLOR,
    DEFAULT_HIGHLIGHT_TEXT_COLOR,
    parse_fa_markup,
    used_highlight_colors,
)
from .translit import translit_to_fa

_HIGHLIGHT_FG_HEX = "#000000"  # همیشه با DEFAULT_HIGHLIGHT_TEXT_COLOR ("black") یکی است


@lru_cache(maxsize=None)
def _resolve_bg_hex(color_name: str, font: str) -> str:
    """رنگِ واقعی‌ای که Pango برای یک نامِ رنگِ پس‌زمینه (مثل «yellow»)
    استفاده می‌کند را با یک رندرِ کوچکِ آزمایشی به‌دست می‌آورد — به‌جای
    حدس‌زدن، چون نگاشتِ نام‌رنگِ Pango با نگاشتِ رنگِ خودِ مانیم یکی
    نیست."""
    probe = MarkupText(f'<span background="{color_name}">x</span>', font=font or "")
    return str(probe.submobjects[0].get_fill_color())


def _merge_highlight_runs(mobject: MarkupText, bg_color_names: set[str], font: str) -> None:
    """هر جعبه‌ی هایلایت را با حروفِ خودش در یک VGroup واحد ادغام
    می‌کند. این کار باعث می‌شود هر تکنیکِ راست‌چین‌کردن که بر پایه‌ی
    برعکس‌کردنِ ``submobjects`` است (چه ``fa_write`` خودمان، چه
    ``Write(..., reverse=True)`` خودِ مانیم) جعبه و متنش را همیشه با هم
    ببیند و از هم جدایشان نکند — نه در ظاهرِ ثابت و نه حینِ انیمیشن."""
    if not bg_color_names:
        return

    bg_hexes = {_resolve_bg_hex(name, font) for name in bg_color_names}
    submobjects = list(mobject.submobjects)
    new_list = []
    i = 0
    n = len(submobjects)
    while i < n:
        sm = submobjects[i]
        color_hex = str(sm.get_fill_color())
        if color_hex in bg_hexes:
            group = [sm]
            j = i + 1
            while j < n and str(submobjects[j].get_fill_color()) == _HIGHLIGHT_FG_HEX:
                group.append(submobjects[j])
                j += 1
            new_list.append(VGroup(*group))
            i = j
        else:
            new_list.append(sm)
            i += 1

    mobject.submobjects = new_list


def FaText(
    text: str,
    font: str | None = None,
    translit: bool = False,
    rtl: bool = True,
    markup: bool = True,
    highlight_color: str = DEFAULT_HIGHLIGHT_COLOR,
    **kwargs,
) -> MarkupText:
    """
    نمایش متن فارسی/عربی در مانیم.

    پارامترها:
        text: متن فارسی (یا فینگلیش، در صورت ``translit=True``). برای
            قالب‌بندیِ بخشی از متن می‌توانید از این نشانه‌ها استفاده کنید:

                **متن**       -> بولد
                *متن*         -> ایتالیک (کج)
                __متن__       -> زیرخط‌دار
                ==متن==       -> هایلایت با رنگ پیش‌فرض
                ==متن|رنگ==   -> هایلایت با رنگ دلخواه

            برای نوشتنِ خودِ نویسه‌های *، _، = به‌صورت عادی، قبلشان یک
            بک‌اسلش بگذارید (مثل ``\\*``).
        font: نام فونت دلخواه. اگر مشخص نشود یا در دسترس نباشد، فونت
            همراه پلاگین («Vazirmatn») استفاده می‌شود.
        translit: اگر True باشد، ورودی به‌عنوان فینگلیش در نظر گرفته
            شده و پیش از رندر به فارسی تبدیل می‌شود (پیش از تفسیر
            نشانه‌های قالب‌بندی).
        rtl: اگر True باشد (پیش‌فرض)، این ترجیح ذخیره می‌شود تا وقتی با
            کمک‌تابع ``fa_write`` انیمیشن نوشتن ساختید، از راست شروع
            شود (طبیعی برای فارسی). ظاهرِ ثابتِ متن (و لایه‌بندیِ
            هایلایت‌ها) را دست‌کاری نمی‌کند — برای انیمیشن‌دادن، از
            ``fa_write(mobject)`` به‌جای ``Write(mobject)`` استفاده کنید.
        markup: اگر False باشد، نشانه‌های بالا نادیده گرفته می‌شوند و
            متن کاملاً خام (بدون تفسیر) نمایش داده می‌شود؛ برای متنی که
            خودش به‌طور طبیعی حاوی *، _ یا = است مفید است.
        highlight_color: رنگ پیش‌فرض برای ``==متن==`` (وقتی رنگ دلخواه
            مشخص نشده باشد).
        **kwargs: هر پارامتر دیگر ``manim.MarkupText`` (مثل
            ``font_size``, ``color``, ``weight``, ``slant``, ...).

    مثال:
        >>> FaText("این **مهم** و این *کج* و این __زیرخط‌دار__ و این ==هایلایت== است.")
    """
    if translit:
        text = translit_to_fa(text)

    highlight_bg_colors: set[str] = set()
    if markup:
        highlight_bg_colors = used_highlight_colors(text, highlight_color=highlight_color)
        text = parse_fa_markup(text, highlight_color=highlight_color)

    resolved_font = resolve_font(font)
    mobject = MarkupText(text, font=resolved_font, **kwargs)

    # هر جعبه‌ی هایلایت را با حروفِ خودش در یک بلوکِ واحد ادغام می‌کنیم
    # (نگاه کنید به ``_merge_highlight_runs``) تا هیچ تکنیکِ راست‌چین‌کردنی
    # (نه مالِ خودمان، نه ``Write(reverse=True)`` خودِ مانیم) نتواند جعبه
    # را از متنش جدا بیندازد.
    _merge_highlight_runs(mobject, highlight_bg_colors, resolved_font)

    mobject._fa_rtl = rtl

    return mobject
