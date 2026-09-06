"""
مقایسه‌ی رفتار پیش‌فرض manim.Text (بدون تعیین فونت -- ممکن است روی
سیستم‌هایی که فونت فارسی ندارند به شکل مربع‌های خالی دربیاید) در برابر
FaText (که همیشه فونتِ فارسیِ همراهِ پلاگین را تضمین می‌کند).

اجرا (دو روش، هرکدام کار می‌کند):
    python demo_comparison.py
    manim -pql demo_comparison.py Comparison
"""

from manim import *
from manim_fa import FaText


class Comparison(Scene):
    def construct(self):
        label1 = Text("manim.Text خام (بدون تعیین فونت):", font_size=24, color=RED)
        label1.to_edge(UP)
        raw = Text("سلام دنیا")  # فونت مشخص نشده -> به فونت پیش‌فرض سیستم وابسته است
        raw.next_to(label1, DOWN, buff=0.4)

        label2 = Text("با FaText (فونت داخلی تضمین‌شده):", font_size=24, color=GREEN)
        label2.next_to(raw, DOWN, buff=0.8)
        fixed = FaText("سلام دنیا", font_size=48)
        fixed.next_to(label2, DOWN, buff=0.4)

        self.add(label1, raw, label2, fixed)
        self.wait(2)


if __name__ == "__main__":
    # این بخش اجازه می‌دهد فایل مستقیماً با «python demo_comparison.py» هم
    # اجرا شود، بدون نیاز به یادگیریِ دستورِ خط‌فرمانِ manim.
    with tempconfig({"quality": "low_quality", "preview": True}):
        Comparison().render()
