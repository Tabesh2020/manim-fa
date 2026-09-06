from manim_fa.markup import parse_fa_markup, has_markup, used_highlight_colors


def test_bold():
    assert parse_fa_markup("این **مهم** است") == "این <b>مهم</b> است"


def test_italic():
    assert parse_fa_markup("این *کج* است") == "این <i>کج</i> است"


def test_underline():
    assert parse_fa_markup("این __زیرخط__ است") == "این <u>زیرخط</u> است"


def test_highlight_default_color():
    assert (
        parse_fa_markup("این ==هایلایت== است")
        == 'این <span background="yellow" foreground="black">هایلایت</span> است'
    )


def test_highlight_custom_color():
    assert (
        parse_fa_markup("==نکته|orange==")
        == '<span background="orange" foreground="black">نکته</span>'
    )


def test_plain_text_unchanged():
    assert parse_fa_markup("بدون هیچ تگی") == "بدون هیچ تگی"


def test_xml_special_chars_escaped():
    assert parse_fa_markup("کاراکتر < و > و &") == "کاراکتر &lt; و &gt; و &amp;"


def test_escaped_literal_asterisk_not_treated_as_markup():
    assert parse_fa_markup(r"3\*4=12") == "3*4=12"


def test_has_markup():
    assert has_markup("این **مهم** است") is True
    assert has_markup("متن ساده") is False


def test_used_highlight_colors():
    assert used_highlight_colors("==الف== و ==ب|red==") == {"yellow", "red"}
    assert used_highlight_colors("متن ساده") == set()
