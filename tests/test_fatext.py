from manim import BOLD, VGroup, Write
from manim_fa import FaText, fa_write


def test_fatext_plain():
    t = FaText("سلام دنیا")
    assert len(t.submobjects) > 0


def test_fatext_bold_no_crash():
    # این دقیقا همان چیزی است که در نسخه‌ی اصلی کرش می‌کرد
    t = FaText("متن پررنگ", weight=BOLD)
    assert len(t.submobjects) > 0


def test_fatext_inline_bold():
    t = FaText("این **مهم** است")
    assert len(t.submobjects) > 0


def test_fatext_markup_disabled():
    # وقتی markup=False است، ** باید عینا در متن بماند نه این‌که بولد شود
    t = FaText("این **نه‌بولد** است", markup=False)
    assert len(t.submobjects) > 0


def test_fatext_highlight_merged_into_single_block():
    # جعبه‌ی هایلایت باید با حروفِ خودش یک VGroup واحد شود، نه چند
    # زیرشیءِ جدا -- تا برعکس‌کردنِ ترتیب هیچ‌وقت آن‌ها را از هم جدا نکند.
    t = FaText("این ==هایلایت== است")
    group_blocks = [sm for sm in t.submobjects if isinstance(sm, VGroup)]
    assert len(group_blocks) == 1
    assert len(group_blocks[0].submobjects) > 1


def test_fatext_no_highlight_no_extra_grouping():
    t = FaText("متن ساده")
    group_blocks = [sm for sm in t.submobjects if isinstance(sm, VGroup)]
    assert len(group_blocks) == 0


def test_fa_write_returns_write_animation():
    t = FaText("سلام ==دنیا==")
    anim = fa_write(t)
    assert isinstance(anim, Write)
    assert anim.reverse is True


def test_fa_write_respects_rtl_false():
    t = FaText("سلام دنیا", rtl=False)
    anim = fa_write(t)
    assert anim.reverse is False


def test_fa_write_explicit_rtl_overrides_stored_value():
    t = FaText("سلام دنیا", rtl=True)
    anim = fa_write(t, rtl=False)
    assert anim.reverse is False
