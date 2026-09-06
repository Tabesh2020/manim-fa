"""
مثالِ پایه‌ای manim-fa.

اجرا (دو روش، هرکدام کار می‌کند):
    python demo.py
    manim -pql demo.py Demo
"""

from manim import *
from manim_fa import FaText, fa_write


class Demo(Scene):
    def construct(self):
        t1 = FaText("به مانیم فارسی خوش آمدید!", font_size=48, color=BLUE)
        t1.to_edge(UP)

        t2 = FaText(
            "این متن ترکیبی است: Hello 123 پایان.",
            font_size=36,
            color=WHITE,
        )
        t2.next_to(t1, DOWN, buff=0.6)

        t3 = FaText("Salam be Manim", translit=True, font_size=40, color=YELLOW)
        t3.next_to(t2, DOWN, buff=0.6)

        t4 = FaText("متن پررنگ (بولد)", font_size=40, weight=BOLD, color=GREEN)
        t4.next_to(t3, DOWN, buff=0.6)

        self.play(fa_write(t1))
        self.play(fa_write(t2))
        self.play(fa_write(t3))
        self.play(fa_write(t4))
        self.wait(1)


if __name__ == "__main__":
    # این بخش اجازه می‌دهد فایل مستقیماً با «python demo.py» هم اجرا شود،
    # بدون نیاز به یادگیریِ دستورِ خط‌فرمانِ manim.
    with tempconfig({"quality": "low_quality", "preview": True}):
        Demo().render()
