"""
Scene R04 —— 例題一：出棧序列（洛谷 P1044）＝ C_n（notes/ran_note015_改寫.pdf 第 5 節）
執行（在 codes/ 內）：manimgl scenes/sceneR04_stack_catalan.py SceneR04StackCatalan

1. n = 3，操作「進進出進出出」：出棧順序 (2,3,1)；每次進棧 +1、出棧 −1，畫成高度不低於 0 的路徑（Dyck 路徑）。
2. 5 種合法操作 ↔ 5 條 Dyck 路徑 ↔ 5 種出棧順序。
3. 前面多加一個 ↑：終點高度 t = 1，條件變成「出發後高度都 > 0」＝ Chu 講義的好路徑。
4. 4 個 ↑、3 個 −1 的排法 C(7,3) = 35，每種恰有一種好讀法，每條好路徑被 7 種讀到：35 = 7 × 5。
   一般 (1/(2n+1))·C(2n+1, n) = C_n = A_1((n),(2))。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import heights, is_good_reading, pop_order, stack_ops_to_steps, stack_sequences
from utils.raney_draw import IntPathMob, level_line
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

N = 3
OPS = "PPOPOO"
ALL = stack_sequences(N)


def check_math():
    assert pop_order(OPS) == (2, 3, 1) and OPS in ALL and len(ALL) == 5
    assert heights(stack_ops_to_steps(OPS)) == [0, 1, 2, 1, 2, 1, 0]
    assert all(min(heights(stack_ops_to_steps(o))) >= 0 for o in ALL)
    up = (1,) + stack_ops_to_steps(OPS)
    assert is_good_reading(up) and heights(up)[1:] == [1, 2, 3, 2, 3, 2, 1]
    from math import comb
    assert comb(7, 3) == 35 == 7 * 5 and raney_A(1, (N,), (2,)) == 5


def ball(k: int) -> VGroup:
    c = Circle(radius=0.27, stroke_color=TEAL_B, stroke_width=3, fill_color=TEAL_E, fill_opacity=0.5)
    return VGroup(c, Tex(str(k), font_size=30).move_to(c))


class SceneR04StackCatalan(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R04　例題一：出棧序列與卡塔蘭數")

        # 1. 棧的動畫
        in_pos = [np.array([3.4 + 0.75 * k, 1.3, 0]) for k in range(N)]
        out_pos = [np.array([-5.0 + 0.75 * k, 1.3, 0]) for k in range(N)]
        st_pos = [np.array([0, 0.5 + 0.66 * k, 0]) for k in range(N)]
        stack = VGroup(Line([-0.42, 2.5, 0], [-0.42, 0.13, 0]), Line([-0.42, 0.13, 0], [0.42, 0.13, 0]),
                       Line([0.42, 0.13, 0], [0.42, 2.5, 0])).set_stroke(GREY_B, 3)
        labels = VGroup(zh("進棧順序", font_size=24, color=GREY_A).move_to(np.array([4.15, 2.1, 0])),
                        zh("棧", font_size=24, color=GREY_A).next_to(stack, UP, buff=0.12),
                        zh("出棧順序", font_size=24, color=GREY_A).move_to(np.array([-4.25, 2.1, 0])))
        balls = [ball(k + 1).move_to(in_pos[k]) for k in range(N)]
        path = IntPathMob(stack_ops_to_steps(OPS), unit=0.48, origin=np.array([-1.45, -2.25, 0]))
        base = level_line(path, 0, 0, 6)
        oplabs = VGroup(*[zh("進" if c == "P" else "出", font_size=22, color=GREY_A)
                          .move_to(np.array([(path.vertex(j)[0] + path.vertex(j + 1)[0]) / 2, path.y_of(0) - 0.35, 0]))
                          for j, c in enumerate(OPS)])
        assert_in_frame(stack, labels, VGroup(*balls), path, oplabs)
        self.say("進棧順序是 ", "$1,2,3$", "；每一步可以「進棧」或「出棧」")
        self.play(ShowCreation(stack), FadeIn(labels), *[FadeIn(b) for b in balls], FadeIn(base), run_time=1.5)
        stk, nxt, nout = [], 0, 0
        for j, c in enumerate(OPS):
            if c == "P":
                b = balls[nxt]
                anim = b.animate.move_to(st_pos[len(stk)])
                stk.append(b)
                nxt += 1
            else:
                b = stk.pop()
                anim = b.animate.move_to(out_pos[nout])
                nout += 1
            self.play(anim, ShowCreation(path.steps[j]), FadeIn(path.dots[j + 1]), FadeIn(oplabs[j]), run_time=0.8)
        self.add(path.dots[0])
        self.say("進棧 ", "$+1$", "、出棧 ", "$-1$", "：棧裡的個數就是高度，永遠 ", "$\\ge 0$")
        self.wait(2.5)

        # 2. 五種操作
        self.play(FadeOut(VGroup(stack, labels, *balls, path, base, oplabs)))
        cells = VGroup()
        for o in ALL:
            p = IntPathMob(stack_ops_to_steps(o), unit=0.3, stroke_width=4, dot_radius=0.035)
            b = level_line(p, 0, 0, 6)
            t = Tex(r"(%s)" % ",".join(map(str, pop_order(o))), font_size=30).next_to(p, DOWN, buff=0.25)
            cells.add(VGroup(p, b, t))
        cells.arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to(0.9 * UP)
        count = Tex(r"C_3=5", font_size=44).next_to(cells, DOWN, buff=0.7)
        assert_in_frame(cells, count)
        self.say("合法的操作 ", "$\\leftrightarrow$", " 不低於 0 的路徑（Dyck 路徑）", "$\\leftrightarrow$", " 出棧順序")
        self.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.2), run_time=2.5)
        self.play(Write(count))
        self.wait(2.5)

        # 3. 前面加一個 ↑
        self.play(FadeOut(VGroup(cells, count)))
        before = IntPathMob(stack_ops_to_steps(OPS), unit=0.45, origin=np.array([-5.6, 0.2, 0]))
        b0 = level_line(before, 0, 0, 6)
        after = IntPathMob((1,) + stack_ops_to_steps(OPS), unit=0.45, origin=np.array([1.0, 0.2, 0]))
        b1 = level_line(after, 0, 0, 7)
        after.steps[0].set_stroke(YELLOW, 6)
        arrow = Arrow(before.get_right() + 0.3 * RIGHT, after.get_left() + 0.3 * LEFT, buff=0.1)
        cap0 = mixed("高度 ", "$\\ge 0$", font_size=26).next_to(before, DOWN, buff=0.45)
        cap1 = mixed("出發後高度 ", "$>0$", "，終點 ", "$t=1$", font_size=26).next_to(after, DOWN, buff=0.45)
        assert_in_frame(before, after, cap0, cap1)
        self.say("在最前面多加一個 ", "$\\uparrow$", "：整條路徑抬高 1")
        self.play(FadeIn(VGroup(before, b0, cap0)))
        self.play(GrowArrow(arrow), FadeIn(VGroup(after, b1)), run_time=1.5)
        self.play(FadeIn(cap1))
        self.say("「", "$\\ge 0$", "」變成「", "$>0$", "」：正是 Chu 講義第 7 節的好路徑")
        self.wait(2.5)

        # 4. 數
        self.play(FadeOut(VGroup(before, b0, cap0, arrow, after, b1, cap1)))
        lines = VGroup(
            mixed("$4$", " 個 ", "$\\uparrow$", "、", "$3$", " 個 ", "$-1$", "：排法 ", "$\\binom{7}{3}=35$", " 種", font_size=30),
            mixed("Raney 引理：每種恰有一種好讀法", font_size=30),
            mixed("每條好路徑被 ", "$7$", " 種（排法, 起點）讀到", font_size=30),
            mixed("$35=7\\times$", "（好路徑數）", "$\\Rightarrow$", " 好路徑數 ", "$=5$", font_size=30),
        ).arrange(DOWN, buff=0.35).move_to(1.1 * UP)
        gen = Tex(r"\frac{1}{2n+1}\binom{2n+1}{n}=\frac{1}{n+1}\binom{2n}{n}=C_n=A_1\big((n),(2)\big)", font_size=40)
        box = boxed(gen, color=YELLOW).next_to(lines, DOWN, buff=0.55)
        assert_in_frame(lines, box)
        self.say("雙重計數：數「（排法, 起點）」的配對")
        self.play(LaggedStartMap(FadeIn, lines, lag_ratio=0.5), run_time=4)
        self.wait(1.5)
        self.say("一般的 ", "$n$", "：拿掉開頭那一步，就回到原來的 Dyck 路徑")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.2)
        self.wait(3)
