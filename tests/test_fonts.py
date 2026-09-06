from manim_fa.fonts import resolve_font, DEFAULT_FONT

def test_default_font_is_always_available():
    assert resolve_font(None) == DEFAULT_FONT
