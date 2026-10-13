"""
Scene 04 —— 重現論文 Fig. 1：n=(1,1)、v=(2,3) 的五種分法

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene04_paper_example.py Scene04PaperExample
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import chords_intersection, label_points, make_circle_points
from utils.counting import closed_form, enumerate_noncrossing
from utils.formulas import create_multinomial_formula
from utils.polygon_groups import dot_color_anims, make_block, make_configuration
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, TYPE1_COLOR, TYPE2_COLOR, zh

N_VEC = (1, 1)
V_VEC = (2, 3)
N_POINTS = 5
TRIANGLE = (0, 1, 2)       # overview 指定：點 1,2,3 形成三角形
CHORD = (3, 4)             # 剩下兩點形成弦
# 交叉的反例：弦的兩端不相鄰
BAD_CHORD = (0, 2)
BAD_TRIANGLE = (1, 3, 4)


def rotated(block, k):
    """把一個群組的點編號順時針轉 k 格。"""
    return tuple(sorted((i + k) % N_POINTS for i in block))


class Scene04PaperExample(ChuScene):
    def construct(self):
        self.show_header("論文的例子（Fig. 1）")
        assert closed_form(N_VEC, V_VEC) == 5 == len(enumerate_noncrossing(N_VEC, V_VEC))

        # ------------------------------------------------------------ Step 1：題目
        vectors = Tex(R"\vec n=(1,\,1),\qquad \vec v=(2,\,3)", font_size=52,
                      t2c={"2": TYPE1_COLOR, "3": TYPE2_COLOR})
        total = Tex(R"N=1\times 2+1\times 3=5", font_size=46)
        top = VGroup(vectors, total).arrange(DOWN, buff=0.4).move_to(0.6 * UP)
        self.play(Write(vectors), run_time=1.2)
        self.say("一條弦（2 個點）加一個三角形（3 個點）")
        self.play(FadeIn(total, shift=0.2 * UP), run_time=0.8)
        self.wait(1.2)
        self.play(
            vectors.animate.scale(0.62).move_to(4.6 * RIGHT + 3.3 * UP),
            total.animate.scale(0.62).move_to(4.6 * RIGHT + 2.7 * UP),
            run_time=0.9,
        )

        # ------------------------------------------------------------ Step 2：圓與 5 個點
        center = 3.3 * LEFT + 0.95 * UP
        radius = 1.75
        circle, dots, coords = make_circle_points(N_POINTS, radius=radius, center=center)
        labels = label_points(coords, center, buff=0.3)
        self.play(ShowCreation(circle), run_time=0.7)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15),
                  FadeIn(labels), run_time=0.9)
        self.say("圓周上 5 個點")
        self.wait(0.6)

        # ------------------------------------------------------------ Step 3：第一種分法
        triangle = make_block(TRIANGLE, coords)
        chord = make_block(CHORD, coords)
        self.say("點 1、2、3 連成三角形，剩下的點 4、5 連成弦")
        self.play(ShowCreation(triangle), *dot_color_anims(dots, TRIANGLE, TYPE2_COLOR), run_time=1.0)
        self.play(ShowCreation(chord), *dot_color_anims(dots, CHORD, TYPE1_COLOR), run_time=0.8)
        self.wait(1.0)

        # ------------------------------------------------------------ Step 4：旋轉五次，收集縮圖
        slots_y = -1.85
        slot_xs = np.linspace(-5.0, 5.0, 5)
        thumb_radius = 0.72
        thumbs = VGroup()
        pattern = VGroup(triangle, chord, dots)      # 點也一起轉，顏色才會跟著群組走
        self.say("把整個圖案沿圓周轉一格，就得到另一種分法")
        for k in range(N_POINTS):
            if k > 0:
                self.play(Rotate(pattern, -TAU / N_POINTS, about_point=center), run_time=0.9)
            thumb = make_configuration(
                N_POINTS, [rotated(TRIANGLE, k), rotated(CHORD, k)],
                radius=thumb_radius, center=np.array([slot_xs[k], slots_y, 0.0]),
            )
            number = Tex(str(k + 1), font_size=30, fill_color=GREY_A).next_to(thumb, DOWN, buff=0.15)
            source = VGroup(circle, triangle, chord, dots).copy()
            self.play(FadeTransform(source, thumb), FadeIn(number), run_time=0.8)
            thumbs.add(VGroup(thumb, number))
            self.wait(0.25)
        self.say("再轉一格就回到第 1 種：一共 5 種分法")
        self.play(Rotate(pattern, -TAU / N_POINTS, about_point=center), run_time=0.9)
        self.wait(1.2)

        # ------------------------------------------------------------ 為什麼只有這 5 種
        self.say("弦的兩端如果不相鄰，三角形一定會穿過它")
        bad_triangle = make_block(BAD_TRIANGLE, coords)
        bad_chord = make_block(BAD_CHORD, coords)
        self.play(
            FadeOut(triangle), FadeOut(chord),
            *dot_color_anims(dots, range(N_POINTS), WHITE),
            run_time=0.5,
        )
        self.play(
            ShowCreation(bad_chord), *dot_color_anims(dots, BAD_CHORD, TYPE1_COLOR), run_time=0.7)
        self.play(
            ShowCreation(bad_triangle), *dot_color_anims(dots, BAD_TRIANGLE, TYPE2_COLOR), run_time=0.8)
        hits = [chords_intersection(coords, BAD_CHORD, edge) for edge in [(1, 3), (1, 4)]]
        rings = VGroup(*[
            Circle(radius=0.17, stroke_color=CROSSING_COLOR, stroke_width=5).move_to(p) for p in hits
        ])
        rings.set_z_index(3)
        bad_tag = VGroup(zh("交叉", font_size=36, color=CROSSING_COLOR),
                         Exmark().set_fill(CROSSING_COLOR)).arrange(RIGHT, buff=0.15)
        bad_tag.next_to(circle, RIGHT, buff=0.5)
        self.play(
            bad_chord.animate.set_stroke(CROSSING_COLOR),
            *dot_color_anims(dots, BAD_CHORD, CROSSING_COLOR),
            ShowCreation(rings),
            *[Flash(p, color=CROSSING_COLOR, flash_radius=0.3) for p in hits],
            FadeIn(bad_tag, shift=0.2 * LEFT),
            run_time=1.0,
        )
        self.wait(1.5)
        self.say("所以弦只能連相鄰的兩點，而相鄰的點對恰有 5 組")
        self.play(
            FadeOut(bad_chord), FadeOut(bad_triangle), FadeOut(rings), FadeOut(bad_tag),
            *dot_color_anims(dots, range(N_POINTS), WHITE),
            run_time=0.6,
        )
        # 依序點亮 5 組相鄰點對
        adjacent = VGroup(*[make_block((i, (i + 1) % N_POINTS), coords) for i in range(N_POINTS)])
        self.play(LaggedStart(*[ShowCreationThenFadeOut(a) for a in adjacent], lag_ratio=0.35),
                  run_time=2.4)
        self.wait(0.4)

        # ------------------------------------------------------------ Step 5：公式
        formula = create_multinomial_formula(N_VEC, V_VEC, font_size=44, steps=True)
        formula.move_to(2.9 * RIGHT + 1.0 * UP)
        if formula.get_width() > 7.2:
            formula.set_width(7.2)
        self.say("代入廣義卡塔蘭數的公式，算出來也是 5")
        self.play(FadeIn(formula, shift=0.6 * LEFT), run_time=1.2)
        self.wait(1.0)
        answer_box = SurroundingRectangle(formula[-1:], buff=0.07, color=YELLOW, stroke_width=3)
        self.play(
            ShowCreation(answer_box),
            LaggedStart(*[ScaleInPlace(t[0], 1.18, rate_func=there_and_back) for t in thumbs],
                        lag_ratio=0.15),
            run_time=1.6,
        )
        self.say("公式的數值，和實際畫出來的分法數目一致")
        self.wait(3.0)
