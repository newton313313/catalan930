"""
Scene 00l —— 卡塔蘭數的生成函數：C = 1 + x C^2

    根（含固定點的那條弦）-> x
    弦內側的配對 -> C，弦外側的配對 -> C（互相獨立 -> 相乘）
    空的配對 -> 1
其他卡塔蘭結構也一樣：根 × 左 × 右。比較 x^n 的係數就是 C_n = sum C_k C_{n-1-k}。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00l_catalan_generating_function.py Scene00lCatalanGeneratingFunction
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    FAMILIES,
    LEFT_COLOR,
    RIGHT_COLOR,
    catalan_item,
)
from utils.circle_points import circle_coords
from utils.counting import binary_trees, catalan, series_square_shift
from utils.polygon_groups import circular_segment
from utils.scene_base import ChuScene
from utils.styles import D_COLOR, MUTED_COLOR, OK_COLOR, ROOT_COLOR, YELLOW, mixed, zh

GF_T2C = {"C(x)": D_COLOR}
CENTER = np.array([-4.2, -0.75, 0.0])
RADIUS = 1.55


def xcc(font_size=40, spaced=True) -> VGroup:
    """「x · C · C」：x 橘（根）、C 青（左）、C 粉紅（右）"""
    parts = [Tex("x", font_size=font_size, fill_color=ROOT_COLOR)]
    if spaced:
        parts.append(Tex(R"\cdot", font_size=font_size))
    parts.append(Tex("C", font_size=font_size, fill_color=LEFT_COLOR))
    if spaced:
        parts.append(Tex(R"\cdot", font_size=font_size))
    parts.append(Tex("C", font_size=font_size, fill_color=RIGHT_COLOR))
    return VGroup(*parts).arrange(RIGHT, buff=0.08)


class Scene00lCatalanGeneratingFunction(ChuScene):
    def construct(self):
        self.show_header("卡塔蘭數的生成函數")
        cs = [catalan(k) for k in range(8)]
        assert series_square_shift(cs) == cs           # 係數真的滿足 C = 1 + x C^2

        # ------------------------------------------------------------ 定義
        definition = Tex(R"C(x)=\sum_{n\ge 0}C_n\,x^n=1+x+2x^2+5x^3+14x^4+\cdots", font_size=48, t2c=GF_T2C)
        definition.move_to(2.45 * UP)
        self.say("把所有大小的卡塔蘭結構收進一個冪級數：", "$x^n$", " 的係數就是 ", "$C_n$")
        self.play(Write(definition), run_time=1.8)
        self.wait(0.8)
        self.say("以圓上的配對為例：", "$x$", " 的次方 ＝ 弦的條數")
        self.wait(1.2)

        # ------------------------------------------------------------ 拆成：根 × 內側 × 外側
        n_ref = 12                                   # 只拿來定位的參考點
        coords = circle_coords(n_ref, RADIUS, CENTER)
        circle = Circle(radius=RADIUS, stroke_color=GREY_C, stroke_width=2.5).move_to(CENTER)
        q = 6                                         # 根弦畫成直徑：內側（右半）、外側（左半）對稱
        inside = circular_segment(0, q, n_ref, RADIUS, CENTER, color=LEFT_COLOR, opacity=0.32)
        outside = circular_segment(q, 0, n_ref, RADIUS, CENTER, color=RIGHT_COLOR, opacity=0.32)
        chord = Line(coords[0], coords[q], stroke_color=ROOT_COLOR, stroke_width=7)
        fixed = Dot(coords[0], radius=0.12, fill_color=ROOT_COLOR).set_z_index(3)
        partner = Dot(coords[q], radius=0.09, fill_color=ROOT_COLOR).set_z_index(3)
        x_lab = Tex("x", font_size=48, fill_color=ROOT_COLOR).next_to(coords[0], UP, buff=0.18)
        c_in = Tex("C", font_size=48, fill_color=LEFT_COLOR).move_to(CENTER + 0.8 * RIGHT)
        c_out = Tex("C", font_size=48, fill_color=RIGHT_COLOR).move_to(CENTER + 0.8 * LEFT)
        note_in = zh("內側：任意的配對", font_size=20, color=LEFT_COLOR)
        note_out = zh("外側：任意的配對", font_size=20, color=RIGHT_COLOR)
        VGroup(note_out, note_in).arrange(RIGHT, buff=0.5).next_to(circle, DOWN, buff=0.2)

        self.say("一個非空的配對：含固定點的那條弦是「根」，記一個 ", "$x$")
        self.play(ShowCreation(circle), FadeIn(fixed), run_time=0.8)
        self.play(ShowCreation(chord), FadeIn(partner), FadeIn(x_lab), run_time=0.9)
        self.wait(0.6)
        self.say("弦的內側、外側各是一個任意大小的配對：各一個 ", "$C$", "，互相獨立")
        self.play(FadeIn(inside), FadeIn(outside), FadeIn(c_in), FadeIn(c_out), FadeIn(note_in),
                  FadeIn(note_out), run_time=1.0)
        self.wait(1.2)

        # 右邊：x · C · C -> x C^2 -> C = 1 + x C^2
        product = xcc(font_size=56).move_to(np.array([2.3, 0.55, 0.0]))
        self.say("獨立的選擇相乘：", "$x\\cdot C\\cdot C$")
        self.play(TransformFromCopy(x_lab, product[0]), FadeIn(product[1]),
                  TransformFromCopy(c_in, product[2]), FadeIn(product[3]),
                  TransformFromCopy(c_out, product[4]), run_time=1.3)
        self.wait(0.8)
        x_c2 = Tex("xC^2", font_size=56, t2c={"x": ROOT_COLOR, "C": D_COLOR}).move_to(product)
        self.play(TransformMatchingShapes(product, x_c2), run_time=1.0)
        self.wait(0.4)
        equation = Tex("C=1+xC^2", font_size=64, t2c={"x": ROOT_COLOR, "C": D_COLOR})
        equation.move_to(np.array([2.3, 0.55, 0.0]))
        empty_note = mixed("1：空的配對（0 條弦）也算一種", font_size=24, color=MUTED_COLOR)
        empty_note.next_to(equation, DOWN, buff=0.45)
        self.say("再加上空的配對（0 條弦）：", "$1$")
        # glyph：C = 1 + x C 2，最後三個是 x、C、2
        self.play(ReplacementTransform(x_c2, equation[-3:]), FadeIn(equation[:-3], shift=0.3 * RIGHT),
                  run_time=1.0)
        self.play(FadeIn(empty_note), run_time=0.5)
        box = SurroundingRectangle(equation, buff=0.25, color=YELLOW, stroke_width=3)
        self.play(ShowCreation(box), run_time=0.6)
        self.say("所以卡塔蘭數的生成函數滿足 ", "$C=1+xC^2$")
        self.wait(1.8)

        # ------------------------------------------------------------ 其他卡塔蘭結構也一樣
        self.play(FadeOut(VGroup(circle, inside, outside, chord, fixed, partner, x_lab, c_in, c_out,
                                 note_in, note_out, empty_note)),
                  VGroup(equation, box).animate.move_to(np.array([0.0, 1.05, 0.0])), run_time=0.9)
        tree = binary_trees(3)[2]
        xs = np.linspace(-5.2, 5.2, 5)
        families = ["triangulation", "parens", "tree", "dyck", "matching"]
        cells = VGroup()
        for x, fam in zip(xs, families):
            item = catalan_item(fam, tree, scale=1.25, colored=True)
            item.move_to(np.array([x, -0.65, 0.0]))
            lab = xcc(font_size=34).next_to(item, DOWN, buff=0.3)
            lab.set_y(-1.85)
            cells.add(VGroup(item, lab))
        self.say("其他卡塔蘭結構也是一樣：一個根（", "$x$", "）× 左邊（", "$C$", "）× 右邊（", "$C$", "）")
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cells], lag_ratio=0.2), run_time=2.2)
        self.wait(2.0)

        # ------------------------------------------------------------ 驗算係數
        self.play(FadeOut(cells), run_time=0.6)
        sq = Tex(R"C^2=(1+x+2x^2+5x^3+\cdots)^2=1+2x+5x^2+14x^3+\cdots", font_size=40, t2c={"C^2": D_COLOR})
        full = Tex(R"1+xC^2=1+x+2x^2+5x^3+14x^4+\cdots", font_size=40, t2c={"C^2": D_COLOR})
        lines = VGroup(sq, full).arrange(DOWN, buff=0.4).move_to(0.65 * DOWN)
        check = mixed("又得到 ", "$1,1,2,5,14,\\ldots$", font_size=28, color=OK_COLOR)
        check.next_to(lines, DOWN, buff=0.3)
        self.say("驗算：把右邊展開，係數正好又是卡塔蘭數")
        self.play(Write(sq), run_time=1.6)
        self.play(Write(full), run_time=1.4)
        self.play(FadeIn(check, shift=0.2 * UP), run_time=0.6)
        self.wait(1.2)
        recurrence = mixed("比較 ", "$x^n$", " 的係數：", "$C_n=\\sum_{k=0}^{n-1}C_kC_{n-1-k}$",
                           "（就是前面的遞迴）", font_size=28)
        recurrence.next_to(lines, DOWN, buff=0.35)
        self.play(FadeOut(check), FadeIn(recurrence), run_time=0.8)
        self.say("方程式和遞迴說的是同一件事")
        self.wait(2.0)
        self.say("問題來了：如果一組不只 2 個點呢？")
        self.wait(2.0)
