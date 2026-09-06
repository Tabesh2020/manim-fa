"""
مثالِ امکاناتِ قالب‌بندیِ جدیدِ manim-fa:
بولد، ایتالیک، زیرخط، هایلایت (با رنگ پیش‌فرض و رنگ دلخواه)، و انیمیشنِ
نوشتنِ راست‌به‌چپِ ``fa_write`` که با هایلایت هم بدون مشکل کار می‌کند.

اجرا (دو روش، هرکدام کار می‌کند):
    python demo_formatting.py
    manim -pql demo_formatting.py FormattingShowcase
"""

from manim import *
from manim_fa import FaText, fa_write


class FormattingShowcase(Scene):
    def construct(self):
        title = FaText("**قابلیت‌های قالب‌بندیِ جدید**", font_size=44, color=BLUE)
        title.to_edge(UP)
        self.play(fa_write(title, run_time=1.2))
        self.wait(0.3)

        # هر خط، یکی از امکانات را جداگانه نشان می‌دهد
        lines = VGroup(
            FaText("این یک متن **بولد** است.", font_size=38),
            FaText("این یک متن *ایتالیک* است.", font_size=38),
            FaText("این یک متن __زیرخط‌دار__ است.", font_size=38),
            FaText("این متن ==هایلایت== شده (رنگ پیش‌فرض).", font_size=38),
            FaText("رنگ دلخواه: ==نکته‌ی مهم|orange==", font_size=38),
        ).arrange(DOWN, buff=0.45, aligned_edge=RIGHT)
        lines.next_to(title, DOWN, buff=0.7)

        for line in lines:
            self.play(fa_write(line, run_time=1.2))
        self.wait(0.5)

        self.play(FadeOut(title), FadeOut(lines))

        # نمونه‌ای که همه‌ی امکانات را با هم ترکیب می‌کند
        combo = FaText(
            "می‌توان **بولد**، *ایتالیک*، __زیرخط__ و ==هایلایت=="
            " را با هم ترکیب کرد.",
            font_size=40,
        )
        combo.width = min(combo.width, config.frame_width - 1)
        self.play(fa_write(combo, run_time=2.5))
        self.wait(1)


if __name__ == "__main__":
    # این بخش اجازه می‌دهد فایل مستقیماً با «python demo_formatting.py» هم
    # اجرا شود، بدون نیاز به یادگیریِ دستورِ خط‌فرمانِ manim.
    with tempconfig({"quality": "low_quality", "preview": True}):
        FormattingShowcase().render()
