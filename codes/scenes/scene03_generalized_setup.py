"""
Scene 03 —— 廣義卡塔蘭問題的設定與 Chu 的定理

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene03_generalized_setup.py Scene03GeneralizedSetup
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import chords_intersection, make_circle_points
from utils.counting import closed_form, enumerate_noncrossing
from utils.formulas import create_multinomial_formula
from utils.polygon_groups import make_block, make_configuration, mark_crossing
from utils.scene_base import ChuScene
from utils.styles import (
    CROSSING_COLOR,
    DOT_RADIUS,
    TYPE1_COLOR,
    TYPE2_COLOR,
    zh,
)

N_VEC = (2, 1)
V_VEC = (2, 3)
N_POINTS = 7
# 範例分法（手動指定）：兩條弦 + 一個三角形
GOOD_BLOCKS = [(0, 1), (4, 5), (2, 3, 6)]
# 交叉的反例：弦 (3,5) 穿過三角形 (2,4,6)
BAD_BLOCKS = [(0, 1), (3, 5), (2, 4, 6)]


def loose_block(points, color):
    """還沒放到圓上的「零散」群組：頂點 + 連線。回傳 (形狀, 點)。"""
    if len(points) == 2:
        shape = Line(points[0], points[1], stroke_color=color, stroke_width=5)
    else:
        shape = Polygon(*points, stroke_color=color, stroke_width=5,
                        fill_color=color, fill_opacity=0.3)
    dots = VGroup(*[Dot(p, radius=DOT_RADIUS, fill_color=color) for p in points])
    dots.set_z_index(2)
    return shape, dots


class Scene03GeneralizedSetup(ChuScene):
    def construct(self):
        self.show_header("廣義卡塔蘭問題")

        # ------------------------------------------------------------ Step 1：兩個向量
        n_gen = Tex(R"\vec n=(n_1,\,n_2,\,\ldots,\,n_k)", font_size=52)
        v_gen = Tex(R"\vec v=(v_1,\,v_2,\,\ldots,\,v_k)", font_size=52)
        n_note = zh("各型群組的「個數」", font_size=28, color=GREY_A)
        v_note = zh("各型群組的「點數」", font_size=28, color=GREY_A)
        n_gen.move_to(3.3 * LEFT + 2.35 * UP)
        v_gen.move_to(3.3 * RIGHT + 2.35 * UP)
        n_note.next_to(n_gen, DOWN, buff=0.25)
        v_note.next_to(v_gen, DOWN, buff=0.25)

        self.play(Write(n_gen), run_time=1.0)
        self.play(FadeIn(n_note, shift=0.15 * UP), run_time=0.5)
        self.play(Write(v_gen), run_time=1.0)
        self.play(FadeIn(v_note, shift=0.15 * UP), run_time=0.5)
        self.say("要 ", "$n_i$", " 個「", "$v_i$", " 點群組」")
        self.wait(1.5)

        n_ex = Tex(R"\vec n=(2,\,1)", font_size=52, t2c={"2": TYPE1_COLOR, "1": TYPE2_COLOR})
        v_ex = Tex(R"\vec v=(2,\,3)", font_size=52, t2c={"2": TYPE1_COLOR, "3": TYPE2_COLOR})
        n_ex.move_to(n_gen)
        v_ex.move_to(v_gen)
        self.play(FadeTransform(n_gen, n_ex), FadeTransform(v_gen, v_ex), run_time=1.0)
        self.say("例：", "$\\vec n=(2,1)$", "、", "$\\vec v=(2,3)$",
                 "，也就是 2 個「2 點群組」與 1 個「3 點群組」")

        # 零散的群組：2 條弦 + 1 個三角形
        y0 = -0.35
        chord1_pts = [np.array([-5.0, y0 - 0.35, 0]), np.array([-3.8, y0 + 0.35, 0])]
        chord2_pts = [np.array([-2.6, y0 - 0.35, 0]), np.array([-1.4, y0 + 0.35, 0])]
        tri_pts = [np.array([2.2, y0 - 0.5, 0]), np.array([3.0, y0 + 0.7, 0]), np.array([3.8, y0 - 0.5, 0])]
        chord1, chord1_dots = loose_block(chord1_pts, TYPE1_COLOR)
        chord2, chord2_dots = loose_block(chord2_pts, TYPE1_COLOR)
        tri, tri_dots = loose_block(tri_pts, TYPE2_COLOR)

        chords_label = zh("2 條弦（每條 2 個點）", font_size=28, color=TYPE1_COLOR)
        chords_label.next_to(VGroup(chord1, chord2), DOWN, buff=0.45)
        tri_label = zh("1 個三角形（3 個點）", font_size=28, color=TYPE2_COLOR)
        tri_label.next_to(tri, DOWN, buff=0.45)
        tri_label.align_to(chords_label, DOWN)

        self.play(
            LaggedStart(
                AnimationGroup(ShowCreation(chord1), FadeIn(chord1_dots)),
                AnimationGroup(ShowCreation(chord2), FadeIn(chord2_dots)),
                lag_ratio=0.4,
            ),
            FadeIn(chords_label, shift=0.15 * UP),
            run_time=1.4,
        )
        self.play(ShowCreation(tri), FadeIn(tri_dots), FadeIn(tri_label, shift=0.15 * UP), run_time=1.0)
        self.wait(1.5)

        # ------------------------------------------------------------ Step 2：總點數
        center = 3.4 * LEFT + 0.45 * DOWN
        radius = 1.8
        circle, dots, coords = make_circle_points(N_POINTS, radius=radius, center=center)
        blocks = VGroup(*[make_block(b, coords) for b in GOOD_BLOCKS])

        self.say("把所有頂點放到同一個圓周上")
        loose_dots = [*chord1_dots, *chord2_dots, *tri_dots]
        target_indices = [*GOOD_BLOCKS[0], *GOOD_BLOCKS[1], *GOOD_BLOCKS[2]]
        self.play(
            FadeOut(chords_label), FadeOut(tri_label),
            FadeOut(n_note), FadeOut(v_note),
            ShowCreation(circle),
            ReplacementTransform(chord1, blocks[0]),
            ReplacementTransform(chord2, blocks[1]),
            ReplacementTransform(tri, blocks[2]),
            *[d.animate.move_to(coords[i]) for d, i in zip(loose_dots, target_indices)],
            run_time=2.0,
        )
        circle_dots = VGroup(*loose_dots)
        config = VGroup(circle, blocks, circle_dots)

        total = Tex(R"N=\langle\vec n,\vec v\rangle=\sum_{i} n_i\,v_i", font_size=50)
        total.move_to(2.6 * RIGHT + 0.75 * UP)
        total_ex = Tex(R"N=2\times 2+1\times 3=7", font_size=50)
        total_ex.next_to(total, DOWN, buff=0.55)
        self.play(Write(total), run_time=1.3)
        self.say("總點數 ", "$N$", " 就是兩個向量的內積")
        self.wait(1.0)
        self.play(FadeIn(total_ex, shift=0.2 * UP), run_time=0.8)
        count_tag = zh("圓上共 7 個點", font_size=28, color=GREY_A).next_to(circle, DOWN, buff=0.3)
        dot_by_index = dict(zip(target_indices, loose_dots))
        in_circle_order = [dot_by_index[i] for i in range(N_POINTS)]
        self.play(
            FadeIn(count_tag),
            LaggedStart(*[Indicate(d, scale_factor=1.9, color=d.get_fill_color())
                          for d in in_circle_order], lag_ratio=0.12),
            run_time=1.6,
        )
        self.wait(1.2)

        # ------------------------------------------------------------ Step 3：定理
        self.play(
            FadeOut(total), FadeOut(total_ex), FadeOut(count_tag),
            n_ex.animate.scale(0.85).move_to(4.6 * LEFT + 2.3 * UP),
            v_ex.animate.scale(0.85).move_to(2.2 * LEFT + 2.3 * UP),
            run_time=0.9,
        )

        thm_title = zh("定理（Chu 1987）", font_size=32, color=YELLOW)
        thm_main = VGroup(
            Tex(R"C_{\vec v}(\vec n)", font_size=58),
            Tex("=", font_size=58),
            zh("不交叉分法的數目", font_size=40),
        ).arrange(RIGHT, buff=0.25)
        thm_detail = VGroup(
            zh("把", font_size=30), Tex(R"\langle\vec n,\vec v\rangle", font_size=40),
            zh("個點分成", font_size=30), Tex("n_i", font_size=40),
            zh("個", font_size=30), Tex("v_i", font_size=40), zh("點群組", font_size=30),
        ).arrange(RIGHT, buff=0.13)
        thm_cond = VGroup(
            zh("而且群組之間不可以", font_size=30),
            zh("交叉", font_size=30, color=CROSSING_COLOR),
        ).arrange(RIGHT, buff=0.1)
        thm = VGroup(thm_title, thm_main, thm_detail, thm_cond).arrange(DOWN, buff=0.35)
        thm.move_to(2.9 * RIGHT + 0.9 * UP)
        thm_box = SurroundingRectangle(thm, buff=0.3, color=YELLOW, stroke_width=3)

        self.say("Chu 的定理：這種分法的數目，就是廣義卡塔蘭數")
        self.play(FadeIn(thm_title), Write(thm_main), run_time=1.4)
        self.play(FadeIn(thm_detail, shift=0.15 * UP), run_time=0.8)
        self.play(FadeIn(thm_cond, shift=0.15 * UP), ShowCreation(thm_box), run_time=0.9)
        self.wait(1.5)

        # 交叉的反例
        bad = make_configuration(N_POINTS, BAD_BLOCKS, radius=radius, center=center)
        mark_crossing(bad.blocks[1])
        for i in BAD_BLOCKS[1]:
            bad.dots[i].set_fill(CROSSING_COLOR)
        # 弦 (3,5) 與三角形的兩條邊 (2,4)、(4,6) 相交：在交點畫紅圈
        rings = VGroup(*[
            Circle(radius=0.2, stroke_color=CROSSING_COLOR, stroke_width=5).move_to(
                chords_intersection(bad.coords, BAD_BLOCKS[1], edge))
            for edge in [(2, 4), (4, 6)]
        ])
        rings.set_z_index(3)
        bad_tag = VGroup(zh("交叉", font_size=34, color=CROSSING_COLOR),
                         Exmark().set_fill(CROSSING_COLOR)).arrange(RIGHT, buff=0.15)
        bad_tag.next_to(bad.circle, DOWN, buff=0.25)
        self.say("像這樣有弦穿過三角形的分法，不算", color=WHITE)
        self.play(FadeOut(config), FadeIn(bad), run_time=0.8)
        self.play(
            ShowCreation(rings), FadeIn(bad_tag, shift=0.15 * UP),
            *[Flash(r.get_center(), color=CROSSING_COLOR, flash_radius=0.3) for r in rings],
            Indicate(thm_cond[1], color=CROSSING_COLOR, scale_factor=1.3),
            run_time=1.0,
        )
        self.wait(1.8)
        self.play(FadeOut(rings), FadeOut(bad_tag), FadeOut(bad), FadeIn(config), run_time=0.8)

        # 公式與數值
        value = closed_form(N_VEC, V_VEC)
        formula = create_multinomial_formula(N_VEC, V_VEC, font_size=40, steps=False)
        formula.next_to(thm_box, DOWN, buff=0.45)
        self.say("代入論文的公式：這個例子共有 ", f"${value}$", " 種分法")
        self.play(Write(formula), run_time=1.5)
        self.wait(0.8)

        # 快速翻過其中幾種（由程式列舉，順序固定，不是亂數）
        all_configs = enumerate_noncrossing(N_VEC, V_VEC)
        assert len(all_configs) == value
        current = config
        shown = [0, 3, 6, 9, 12, 15, 18, 20]
        tag = None
        for idx in shown:
            new = make_configuration(N_POINTS, all_configs[idx], radius=radius, center=center)
            new_tag = Tex(fR"{idx + 1}\,/\,{value}", font_size=36, fill_color=GREY_A)
            new_tag.next_to(new.circle, DOWN, buff=0.25)
            self.remove(current)
            if tag is not None:
                self.remove(tag)
            self.add(new, new_tag)
            current, tag = new, new_tag
            self.wait(0.45)
        self.wait(2.5)
