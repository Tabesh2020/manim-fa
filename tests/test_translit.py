from manim_fa.translit import translit_to_fa

def test_basic_word():
    assert translit_to_fa("salam") == "سالام"

def test_numbers_converted_by_default():
    assert translit_to_fa("123") == "۱۲۳"
