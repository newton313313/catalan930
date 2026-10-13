"""
Scene 07 —— 遞迴變成生成函數方程：D = 1 + x_1 D^{v_1} + ... + x_k D^{v_k}（論文式 (6)）

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene07_generating_function.py Scene07GeneratingFunction
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan, closed_form
from utils.formulas import GF_T2C, gf_definition
from utils.root_figure import ROOT_N_VEC, ROOT_V_VEC, RootFigure, block_icon
from utils.scene_base import ChuScene
from utils.styles import (
    D_COLOR,
    GENERIC_COLOR,
    REGION_COLORS,
    TYPE1_COLOR,
    TYPE2_COLOR,
    zh,
)

EQ_STRING = R"D=1+x_1D^{v_1}+x_2D^{v_2}+\cdots+x_kD^{v_k}"
EQ_TERMS = [R"x_1D^{v_1}", R"x_2D^{v_2}", R"x_kD^{v_k}"]


class Scene07GeneratingFunction(ChuScene):
    def construct(self):
        self.show_header("生成函數")

        # ------------------------------------------------------------ Step 1：定義
        definition = gf_definition(font_size=54)
        definition.move_to(1.9 * UP)
        self.play(Write(definition), run_time=2.0)
        self.say("生成函數 ", "$D$", "：把所有的 ", "$d(\\vec n)$", " 收進同一個冪級數",
                 t2c={"D": D_COLOR})
        self.wait(1.5)

        # x_i 是記帳用的變數
        coeff = closed_form(ROOT_N_VEC, ROOT_V_VEC)       # d(3,2) = 990
        mono = Tex(fR"{coeff}\,x_1^{{3}}\,x_2^{{2}}", font_size=84,
                   isolate=[str(coeff), R"x_1^{3}", R"x_2^{2}"],
                   t2c={R"x_1^{3}": TYPE1_COLOR, R"x_2^{2}": TYPE2_COLOR})
        mono.move_to(0.1 * UP)
        part_c, part_1, part_2 = mono[str(coeff)][0], mono[R"x_1^{3}"][0], mono[R"x_2^{2}"][0]

        note_c = zh(f"這種情況共 {coeff} 種分法", font_size=26, color=GREY_A)
        note_1 = VGroup(
            VGroup(*[block_icon(2) for _ in range(3)]).arrange(RIGHT, buff=0.2),
            zh("3 條弦", font_size=26, color=TYPE1_COLOR),
        ).arrange(DOWN, buff=0.2)
        note_2 = VGroup(
            VGroup(*[block_icon(3) for _ in range(2)]).arrange(RIGHT, buff=0.2),
            zh("2 個三角形", font_size=26, color=TYPE2_COLOR),
        ).arrange(DOWN, buff=0.2)
        notes = VGroup(note_c, note_1, note_2).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
        notes.move_to(1.75 * DOWN)
        links = VGroup(*[
            Line(part.get_bottom() + 0.12 * DOWN, note.get_top() + 0.12 * UP,
                 stroke_color=GREY_B, stroke_width=2)
            for part, note in zip([part_c, part_1, part_2], [note_c, note_1, note_2])
        ])

        self.say("$x_i$", " 是記帳的變數：每用一個第 ", "$i$", " 型群組，就乘一個 ", "$x_i$")
        self.play(FadeIn(mono, shift=0.2 * UP), run_time=0.9)
        self.play(ShowCreation(links[1]), FadeIn(note_1, shift=0.2 * UP), run_time=0.8)
        self.play(ShowCreation(links[2]), FadeIn(note_2, shift=0.2 * UP), run_time=0.8)
        self.play(ShowCreation(links[0]), FadeIn(note_c, shift=0.2 * UP), run_time=0.8)
        self.wait(2.0)

        # ------------------------------------------------------------ Step 2：幾何 <-> 代數
        self.play(
            FadeOut(mono), FadeOut(notes), FadeOut(links),
            definition.animate.scale(0.62).move_to(3.0 * UP + 1.2 * RIGHT),
            run_time=0.9,
        )
        fig = RootFigure(center=4.1 * LEFT + 0.15 * UP, radius=1.8, label_font_size=38)
        self.play(FadeIn(fig), run_time=0.9)
        self.say("回想上一幕的分解：一段對應一個 ", "$D$", t2c={"D": D_COLOR})

        x0 = 2.6
        d_letters = VGroup(*[Tex("D", font_size=80, fill_color=REGION_COLORS[j]) for j in range(3)])
        times = VGroup(*[Tex(R"\times", font_size=56) for _ in range(2)])
        row = VGroup(d_letters[0], times[0], d_letters[1], times[1], d_letters[2])
        row.arrange(RIGHT, buff=0.35).move_to(x0 * RIGHT + 1.3 * UP)
        self.play(
            LaggedStart(*[TransformFromCopy(fig.region_labels[j], d_letters[j]) for j in range(3)],
                        lag_ratio=0.3),
            FadeIn(times),
            run_time=1.6,
        )
        self.wait(0.6)

        d_cubed = Tex("D^{3}", font_size=88, t2c={"D": D_COLOR}).move_to(x0 * RIGHT + 1.3 * UP)
        self.say("3 段獨立的區域相乘：", "$D^3$", t2c={"D": D_COLOR})
        self.play(ReplacementTransform(row, d_cubed), run_time=1.0)
        self.wait(0.6)

        d_general = Tex("D^{v_i}", font_size=88, t2c={"D": D_COLOR, "v_i": TYPE2_COLOR})
        d_general.move_to(d_cubed)
        self.say("$v_i$", " 段獨立的區域：", "$D^{v_i}$", t2c={"D": D_COLOR, "v_i": TYPE2_COLOR})
        self.play(FadeTransform(d_cubed, d_general), run_time=0.9)
        self.wait(0.6)

        x_i = Tex("x_i", font_size=88, fill_color=TYPE2_COLOR)
        term = VGroup(x_i, d_general.copy()).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        x_i.shift(0.1 * DOWN)
        term.move_to(x0 * RIGHT + 0.7 * DOWN)
        term_box = SurroundingRectangle(term, buff=0.22, color=YELLOW, stroke_width=3)
        self.say("根群組是一個第 ", "$i$", " 型群組：再乘上 ", "$x_i$", t2c={"x_i": TYPE2_COLOR})
        self.play(Indicate(fig.root, scale_factor=1.06, color=TYPE2_COLOR), run_time=0.8)
        self.play(TransformFromCopy(fig.root, x_i), TransformFromCopy(d_general, term[1]), run_time=1.2)
        self.play(ShowCreation(term_box), run_time=0.6)
        self.wait(1.5)

        # ------------------------------------------------------------ Step 3：各種型別的項飛進來
        self.play(
            FadeOut(fig), FadeOut(d_general), FadeOut(term), FadeOut(term_box),
            run_time=0.8,
        )
        eq = Tex(EQ_STRING, font_size=68, isolate=[*EQ_TERMS, R"\cdots"],
                 t2c={"D": D_COLOR, **GF_T2C})
        eq.move_to(0.1 * UP)
        term_mobs = [eq[t][0] for t in EQ_TERMS]
        dots_mob = eq[R"\cdots"][0]
        lhs = VGroup(eq[0], eq[1])      # "D" 與 "="
        one = eq[2]                     # 常數項 "1"
        plus_signs = eq["+"]            # 四個加號，由左到右

        icons = VGroup(
            block_icon(2, radius=0.34),
            block_icon(3, radius=0.34),
            block_icon(5, radius=0.34, color=GENERIC_COLOR),
        )
        names = VGroup(
            zh("根群組是弦", font_size=22, color=TYPE1_COLOR),
            zh("根群組是三角形", font_size=22, color=TYPE2_COLOR),
            zh("根群組是第 k 型", font_size=22, color=GENERIC_COLOR),
        )
        for icon, name, t_mob in zip(icons, names, term_mobs):
            icon.next_to(t_mob, UP, buff=0.45)
            name.next_to(t_mob, DOWN, buff=0.4)

        self.say("固定點所在的群組可以是任何一型：每一型給出一項")
        directions = [4 * LEFT, 3 * UP, 4 * RIGHT]
        for j in range(3):
            if j == 2:
                self.play(FadeIn(dots_mob), run_time=0.4)
            self.play(
                FadeIn(term_mobs[j], shift=-directions[j] * 0.6),
                FadeIn(icons[j], shift=-directions[j] * 0.6),
                FadeIn(names[j]),
                run_time=1.0,
            )
            self.wait(0.4)
        self.say("不同的情況互不重疊，所以相加")
        self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in plus_signs[1:]], lag_ratio=0.2), run_time=0.9)
        self.wait(0.8)

        one_name = zh("空的分法", font_size=22, color=GREY_A).next_to(one, DOWN, buff=0.4)
        one_name.align_to(names[0], DOWN)
        self.say("還有一種情況：圓上沒有任何點。這個「空的分法」貢獻常數 1")
        self.play(FadeIn(one, scale=1.6), FadeIn(plus_signs[0]), FadeIn(one_name), run_time=0.9)
        self.wait(1.0)

        self.say("全部加起來，就是 ", "$D$", " 本身", t2c={"D": D_COLOR})
        self.play(FadeIn(lhs, shift=0.3 * RIGHT), run_time=0.8)
        eq_box = SurroundingRectangle(eq, buff=0.3, color=YELLOW, stroke_width=4)
        eq_tag = zh("論文式 (6)", font_size=26, color=GREY_A).next_to(eq_box, RIGHT, buff=0.2)
        eq_tag.next_to(eq_box, UP, buff=0.15).align_to(eq_box, RIGHT)
        self.play(
            FadeOut(icons), FadeOut(names), FadeOut(one_name),
            ShowCreation(eq_box), FadeIn(eq_tag),
            run_time=1.0,
        )
        self.say("這條方程和上一幕的遞迴是同一件事，只是換成代數的語言")
        self.wait(3.5)

        # ------------------------------------------------------------ Step 4：回到經典情形檢查
        eq_group = VGroup(eq, eq_box, eq_tag)
        self.play(eq_group.animate.scale(0.75).move_to(1.55 * UP), run_time=0.9)
        special_tag = VGroup(
            zh("檢查：只有弦的情形", font_size=30, color=TYPE1_COLOR),
            Tex(R"(k=1,\ v_1=2)", font_size=38, fill_color=TYPE1_COLOR),
        ).arrange(RIGHT, buff=0.25).move_to(0.1 * DOWN)
        special = Tex(R"D=1+xD^{2}", font_size=64, t2c={"D": D_COLOR, "x": TYPE1_COLOR})
        special.move_to(1.15 * DOWN)
        self.say("檢查：如果只有弦，方程變成 ", "$D=1+xD^2$", t2c={"D": D_COLOR, "x": TYPE1_COLOR})
        self.play(FadeIn(special_tag, shift=0.2 * UP), run_time=0.7)
        self.play(Write(special), run_time=1.2)
        self.wait(1.0)

        cats = [catalan(m) for m in range(5)]
        assert cats == [1, 1, 2, 5, 14]
        series = Tex(R"D=1+x+2x^{2}+5x^{3}+14x^{4}+\cdots", font_size=60,
                     t2c={"D": D_COLOR, "x": TYPE1_COLOR})
        series.move_to(2.3 * DOWN)
        self.play(FadeIn(series, shift=0.3 * UP), run_time=1.0)
        self.say("解出來的係數 1, 1, 2, 5, 14, … 正是卡塔蘭數")
        self.wait(3.5)
