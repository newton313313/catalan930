"""
Scene R02 —— 為什麼恰有一種：最後一個最低點（notes/ran_note015_改寫.pdf 第 3 節）
執行（在 codes/ 內）：manimgl scenes/sceneR02_last_minimum.py SceneR02LastMinimum

1. 把 x = (2,−1,−3,1,2) 無限重複：S_{i+M} = S_i + 1（原筆記第 19 行下標錯一位，這裡用正確的式子）。
2. 存在：前 M 點的最後一個最低點 x = 3；從那裡讀，之後每點都比它高。
3. 唯一：y = 1（讀到第 x 點相對高度 −4）、y = 4（讀到第 x+M 點相對高度 0）；關鍵是整數：S_y > S_x ⇒ S_y ≥ S_x + 1。
4. 好幾個最低點：(−1,1,−1,2) 取最後一個；較早的那個讀到第 3 點高度 0。
5. 整數不能少：(1/2,1/2) 兩種讀法都好；一般的 t 要每步最多上升 1：(2,0) 總和 2 卻只有 1 種好讀法。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import NOTE015_SEQ, good_starts, heights, last_minimum, periodic_heights, positive_count, reading
from utils.raney_draw import IntPathMob, level_line
from utils.scene_base import ChuScene
from utils.styles import mixed, zh

SEQ = NOTE015_SEQ
M = len(SEQ)
TWO_MIN = (-1, 1, -1, 2)
MARK = MAROON_B


def check_math():
    S = periodic_heights(SEQ, 3)
    assert S[:6] == [0, 2, 1, -2, -1, 1] and all(S[i + M] == S[i] + 1 for i in range(10))
    assert last_minimum(SEQ) == 3 and all(S[k] > S[3] for k in range(4, 9))
    assert S[3] - S[1] == -4 and S[8] - S[4] == 0
    assert heights(TWO_MIN) == [0, -1, 0, -1, 1] and last_minimum(TWO_MIN) == 3
    assert heights(reading(TWO_MIN, 3))[1:] == [2, 1, 2, 1]
    assert good_starts(TWO_MIN) == [3] and heights(reading(TWO_MIN, 1))[1:] == [1, 0, 2, 1]
    from fractions import Fraction
    half = (Fraction(1, 2), Fraction(1, 2))
    assert [positive_count(reading(half, i)) for i in range(2)] == [2, 2]
    assert [positive_count(reading((2, 0), i)) == 2 for i in range(2)] == [True, False]


def dot_at(path, j, color=MARK, r=0.09):
    return Dot(path.vertex(j), radius=r, fill_color=color).set_z_index(3)


class SceneR02LastMinimum(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R02　為什麼恰有一種：最後一個最低點")

        # 1. 無限重複
        path = IntPathMob(SEQ * 3, unit=0.38, origin=np.array([-6.2, -0.2, 0]))
        base = level_line(path, 0, 0, 3 * M)
        seps = VGroup(*[DashedLine(np.array([path.vertex(k)[0], path.y_of(-2.6), 0]),
                                   np.array([path.vertex(k)[0], path.y_of(4.6), 0]), stroke_color=GREY_D)
                        for k in (M, 2 * M)])
        ups = VGroup(*[Tex(r"+1", font_size=28, fill_color=YELLOW).next_to(path.vertex(k), DR, buff=0.06)
                       for k in (M, 2 * M, 3 * M)])
        law = Tex(r"S_{i+M}=S_i+x_{i+1}+\cdots+x_{i+M}=S_i+1", font_size=34).move_to(np.array([3.3, 2.3, 0]))
        assert_in_frame(path, seps, law)
        self.say("把序列一直重複下去：每走一個週期，高度上升 1")
        self.play(FadeIn(base), FadeIn(seps), ShowCreation(path.steps, lag_ratio=1), FadeIn(path.dots), run_time=4)
        self.play(LaggedStartMap(FadeIn, ups, lag_ratio=0.3), Write(law), run_time=1.8)
        self.wait(2)

        # 2. 存在：最後一個最低點
        first = VGroup(*[dot_at(path, j, GREY_A, 0.07) for j in range(1, M + 1)])
        self.say("在第 ", "$1$", " 到 ", "$M$", " 點中找最低點（有好幾個就取最後一個）")
        self.play(LaggedStartMap(FadeIn, first, lag_ratio=0.15))
        xdot = dot_at(path, 3)
        xlab = Tex(r"x=3", font_size=30, fill_color=MARK).next_to(xdot, DOWN, buff=0.15)
        self.play(FadeOut(first), FadeIn(xdot, scale=1.5), FadeIn(xlab))
        floor = level_line(path, -2, 3, 3 * M, color=MARK)
        shade = Rectangle(width=M * 0.38, height=7.4 * 0.38, stroke_width=0, fill_color=YELLOW, fill_opacity=0.12)
        shade.move_to(np.array([(path.vertex(3)[0] + path.vertex(3 + M)[0]) / 2, path.y_of(1.0), 0]))
        why = VGroup(
            mixed("$k\\le M$", "：", "$x$", " 是最後一個最低點", font_size=26),
            mixed("$\\Rightarrow S_k>S_x$", font_size=26),
            mixed("$k>M$", "：", "$S_k=S_{k-M}+1\\ge S_x+1$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(np.array([3.4, 0.5, 0]))
        assert_in_frame(why, shade)
        assert_apart(why, path)
        self.say("從第 ", "$x$", " 點開始讀一圈：之後每一點都比它高，所以是好讀法")
        self.play(FadeIn(shade), ShowCreation(floor), run_time=1.5)
        self.play(FadeIn(why, shift=0.2 * LEFT), run_time=1.2)
        self.wait(3)

        # 3. 唯一
        self.play(FadeOut(VGroup(why, shade, floor, law, ups)))
        self.say("換一個起點 ", "$y$", "：若 ", "$S_y>S_x$", "，因為是整數，", "$S_y\\ge S_x+1$")
        key = mixed("$S_y>S_x$", "（整數）", "$\\Rightarrow S_y\\ge S_x+1$", font_size=30, color=YELLOW)
        key.move_to(np.array([3.3, 2.4, 0]))
        self.play(FadeIn(key))
        self.wait(1.5)
        cases = []
        for y, bad, txt in [(1, 3, ["$y=1<x$", "：讀到第 ", "$x$", " 點，高度 ", "$S_x-S_y=-4<0$"]),
                            (4, 8, ["$y=4>x$", "：讀到第 ", "$x+M$", " 點，高度 ", "$S_x+1-S_y=0$"])]:
            ydot = dot_at(path, y, TEAL)
            line = level_line(path, path.heights[y], y, bad + 0.6, color=TEAL)
            bdot = dot_at(path, bad, RED, 0.1)
            cap = mixed(*txt, font_size=26).move_to(np.array([0, -1.75 if y == 1 else -2.4, 0]))
            assert_in_frame(cap)
            self.play(FadeIn(ydot, scale=1.5), ShowCreation(line), run_time=1)
            self.play(FadeIn(bdot, scale=1.6), FadeIn(cap), run_time=1)
            self.wait(2)
            cases.append(VGroup(ydot, line, bdot, cap))
        self.say("所以只有從 ", "$x$", " 開始讀才是好讀法")
        self.wait(2)

        # 4. 好幾個最低點
        self.play(FadeOut(VGroup(path, base, seps, xdot, xlab, key, *cases)))
        p2 = IntPathMob(TWO_MIN * 2, unit=0.6, origin=np.array([-5.8, 0.4, 0]))
        b2 = level_line(p2, 0, 0, 8)
        m1, m3 = dot_at(p2, 1, GREY_A), dot_at(p2, 3, MARK)
        l1 = Tex(r"1", font_size=28).next_to(m1, DOWN, buff=0.12)
        l3 = Tex(r"3", font_size=28, fill_color=MARK).next_to(m3, DOWN, buff=0.12)
        t2 = mixed("$x=(-1,1,-1,2)$", "：第 1、3 點一樣低", font_size=28).move_to(np.array([2.6, 2.0, 0]))
        r3 = mixed("從第 3 點讀：", "$2,1,2,1$", " ✓", font_size=28).next_to(t2, DOWN, aligned_edge=LEFT, buff=0.35)
        r1 = mixed("從第 1 點讀：", "$1,0,2,1$", " ✗", font_size=28).next_to(r3, DOWN, aligned_edge=LEFT, buff=0.25)
        hit = dot_at(p2, 3, RED, 0.1)
        assert_in_frame(p2, t2, r3, r1)
        assert_apart(VGroup(t2, r3, r1), p2)
        self.say("有好幾個最低點時，取最後一個")
        self.play(FadeIn(b2), ShowCreation(p2.steps, lag_ratio=1), FadeIn(p2.dots), run_time=2)
        self.play(FadeIn(VGroup(m1, m3, l1, l3)), FadeIn(t2))
        self.play(FadeIn(r3))
        self.say("較早的那個不行：讀到第 3 點時高度剛好是 0")
        self.play(FadeIn(r1), FadeIn(hit, scale=1.6))
        self.wait(2.5)

        # 5. 整數不能少；一般的 t
        self.play(FadeOut(VGroup(p2, b2, m1, m3, l1, l3, t2, r3, r1, hit)))
        half = VGroup(zh("不是整數", font_size=30, color=YELLOW),
                      mixed("$x=(\\tfrac12,\\tfrac12)$", font_size=28),
                      mixed("兩種讀法都是好讀法", font_size=26)).arrange(DOWN, buff=0.3)
        gen = VGroup(zh("總和是 2", font_size=30, color=YELLOW),
                     mixed("$x=(2,0)$", font_size=28),
                     mixed("只有 1 種好讀法，不是 2 種", font_size=26)).arrange(DOWN, buff=0.3)
        VGroup(half, gen).arrange(RIGHT, buff=2.2).move_to(1.2 * UP)
        pa = VGroup(*[IntPathMob(r, unit=1.0, stroke_width=4) for r in [(0.5, 0.5), (0.5, 0.5)]]).arrange(RIGHT, buff=0.7)
        pb = VGroup(*[IntPathMob(r, unit=0.5, stroke_width=4) for r in [(2, 0), (0, 2)]]).arrange(RIGHT, buff=0.7)
        pa.next_to(half, DOWN, buff=0.45)
        pb.next_to(gen, DOWN, buff=0.45)
        assert_in_frame(half, gen, pa, pb)
        self.say("唯一性用到「整數」；一般的終點高度 ", "$t$", " 還要每步最多上升 1")
        self.play(FadeIn(half), FadeIn(pa))
        self.wait(1.5)
        self.play(FadeIn(gen), FadeIn(pb))
        self.wait(3)
