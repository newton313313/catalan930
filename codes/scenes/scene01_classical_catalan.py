"""
Scene 01 —— 經典卡塔蘭數：圓周上 2n 個點的不交叉配對

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene01_classical_catalan.py Scene01ClassicalCatalan
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import chord_between, chords_intersection, label_points, make_circle_points
from utils.formulas import catalan_formula
from utils.polygon_groups import dot_color_anims, make_configuration
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, OK_COLOR, TYPE1_COLOR, boxed, zh

# n = 3 時全部 5 種不交叉配對（點編號 0..5，順時針）
ALL_MATCHINGS_N3 = [
    [(0, 1), (2, 3), (4, 5)],
    [(0, 1), (2, 5), (3, 4)],
    [(0, 3), (1, 2), (4, 5)],
    [(0, 5), (1, 2), (3, 4)],
    [(0, 5), (1, 4), (2, 3)],
]
GOOD_PAIRING = [(0, 1), (2, 5), (3, 4)]     # overview 指定的 (1,2),(3,6),(4,5)
BAD_PAIRING = [(0, 3), (1, 4), (2, 5)]      # overview 指定的 (1,4),(2,5),(3,6)


class Scene01ClassicalCatalan(ChuScene):
    def construct(self):
        # ------------------------------------------------------------ 標題 -> 公式
        title = zh("卡塔蘭數", font_size=76)
        subtitle = zh("Catalan numbers", font_size=36, color=GREY_B)
        VGroup(title, subtitle).arrange(DOWN, buff=0.35)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=0.2 * UP), run_time=0.6)
        self.wait(0.8)

        formula = catalan_formula(font_size=76)
        values = Tex(R"C_0,\ C_1,\ C_2,\ \ldots\ =\ 1,\ \ 1,\ \ 2,\ \ 5,\ \ 14,\ \ 42,\ \ \ldots",
                     font_size=40, fill_color=GREY_A)
        values.next_to(formula, DOWN, buff=0.7)
        self.play(FadeOut(subtitle), FadeTransform(title, formula), run_time=1.0)
        self.play(FadeIn(values, shift=0.2 * UP), run_time=0.7)
        self.wait(1.5)
        self.play(
            FadeOut(values),
            formula.animate.scale(0.5).to_corner(UL, buff=0.4),
            run_time=1.0,
        )

        # ------------------------------------------------------------ 圓與 2n 個點
        center = 0.2 * UP
        radius = 2.3
        circle, dots, coords = make_circle_points(6, radius=radius, center=center)
        labels = label_points(coords, center)
        self.play(ShowCreation(circle), run_time=0.9)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15), run_time=1.0)
        self.say("圓周上放 ", "$2n$", " 個點（這裡 ", "$n=3$", "，共 6 個點）")
        self.play(FadeIn(labels), run_time=0.5)
        self.wait(1.0)

        # ------------------------------------------------------------ A. 不交叉的配對
        self.say("用 ", "$n$", " 條弦把這些點兩兩配對")
        good_chords = VGroup(*[chord_between(coords, i, j) for i, j in GOOD_PAIRING])
        for chord, pair in zip(good_chords, GOOD_PAIRING):
            self.play(ShowCreation(chord), *dot_color_anims(dots, pair, TYPE1_COLOR), run_time=0.7)
        ok_tag = VGroup(zh("不交叉", font_size=42, color=OK_COLOR),
                        Checkmark().set_fill(OK_COLOR).scale(1.2)).arrange(RIGHT, buff=0.2)
        ok_tag.next_to(circle, RIGHT, buff=1.0)
        self.play(FadeIn(ok_tag, shift=0.3 * LEFT), run_time=0.6)
        self.say("這三條弦在圓內互不相交：算一種")
        self.wait(1.5)

        # ------------------------------------------------------------ B. 交叉的配對
        self.play(FadeOut(good_chords), FadeOut(ok_tag),
                  *dot_color_anims(dots, range(6), WHITE), run_time=0.6)
        self.say("換一種配法……")
        bad_chords = VGroup(*[chord_between(coords, i, j) for i, j in BAD_PAIRING])
        for chord, pair in zip(bad_chords, BAD_PAIRING):
            self.play(ShowCreation(chord), *dot_color_anims(dots, pair, TYPE1_COLOR), run_time=0.6)
        cross_point = chords_intersection(coords, BAD_PAIRING[0], BAD_PAIRING[1])
        bad_tag = VGroup(zh("交叉", font_size=42, color=CROSSING_COLOR),
                         Exmark().set_fill(CROSSING_COLOR).scale(1.2)).arrange(RIGHT, buff=0.2)
        bad_tag.next_to(circle, RIGHT, buff=1.0)
        ring = Circle(radius=0.28, stroke_color=CROSSING_COLOR, stroke_width=5).move_to(cross_point)
        self.play(
            bad_chords.animate.set_stroke(CROSSING_COLOR),
            *dot_color_anims(dots, range(6), CROSSING_COLOR),
            Flash(cross_point, color=CROSSING_COLOR, flash_radius=0.45, line_length=0.3),
            ShowCreation(ring),
            FadeIn(bad_tag, shift=0.3 * LEFT),
            run_time=1.0,
        )
        self.say("弦在圓內相交：這種配法不算")
        self.wait(1.5)
        self.play(FadeOut(bad_chords), FadeOut(ring), FadeOut(bad_tag),
                  *dot_color_anims(dots, range(6), WHITE), run_time=0.6)

        # ------------------------------------------------------------ C. 全部 5 種
        self.say("$n=3$", " 時，不交叉的配對一共有 5 種")
        big = VGroup(circle, dots, labels)
        thumbs = VGroup(*[
            make_configuration(6, m, radius=0.95) for m in ALL_MATCHINGS_N3
        ]).arrange(RIGHT, buff=0.55).move_to(0.9 * UP)
        numbers = VGroup(*[
            Tex(str(k + 1), font_size=34, fill_color=GREY_A).next_to(t, DOWN, buff=0.25)
            for k, t in enumerate(thumbs)
        ])
        self.play(FadeOut(big, scale=0.6), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(VGroup(t, num), scale=0.7) for t, num in zip(thumbs, numbers)],
                        lag_ratio=0.3),
            run_time=2.2,
        )
        count = Tex(R"C_3=\frac{1}{4}\binom{6}{3}=\frac{20}{4}=5", font_size=52)
        count.next_to(numbers, DOWN, buff=0.55)
        self.play(Write(count), run_time=1.2)
        self.wait(1.5)

        # ------------------------------------------------------------ 結論
        statement = VGroup(
            Tex(R"C_n\;=", font_size=56),
            zh("圓周上 2n 個點的「不交叉配對」數目", font_size=38),
        ).arrange(RIGHT, buff=0.3)
        statement_box = boxed(statement, color=TYPE1_COLOR, buff=0.3)
        statement_box.move_to(count)
        self.play(FadeOut(count), run_time=0.4)
        self.play(FadeIn(statement), ShowCreation(statement_box[0]), run_time=1.0)
        self.say("這是 Motzkin 的結果，也是 Chu 這篇論文要推廣的起點")
        self.wait(3.0)
