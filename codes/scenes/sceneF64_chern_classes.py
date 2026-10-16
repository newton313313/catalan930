"""
Scene F64 —— Chern 類：為什麼 e_k = 0（Fulton §B.4，書 p.222–225；接第 10 章命題 3、Lemma 9）
執行（在 codes/ 內）：manimgl scenes/sceneF64_chern_classes.py SceneF64ChernClasses
"""
import sys
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import betti_from_cells, chern_projective
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.scene_base import ChuScene
from utils.schubert import divided_difference, poly_str, staircase_monomials
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import elementary_e, poly_mul, poly_sum

SLOW = 8.0
OK = "#7CE38B"
L_COLORS = [TEAL, PINK, GOLD]


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def hpoly(coeffs):
    out = []
    for k, c in enumerate(coeffs):
        mono = "" if k == 0 else "h" if k == 1 else "h^{%d}" % k
        out.append((str(c) if c != 1 or not mono else "") + mono)
    return "+".join(out)


def one_minus_product(m):
    f = {(0,) * m: 1}
    for i in range(m):
        e = [0] * m
        e[i] = 1
        f = poly_mul(f, {(0,) * m: 1, tuple(e): -1})
    return f


def mono_tex(e):
    s = "".join("x_%d" % (i + 1) + ("^{%d}" % k if k > 1 else "") for i, k in enumerate(e) if k)
    return s or "1"


def check_math():
    for n in (1, 2, 3):
        c = chern_projective(n)
        assert c == [comb(n + 1, k) for k in range(n + 1)]
        assert c[n] == n + 1 == betti_from_cells([1] * (n + 1))[1]          # c_n = χ(P^n)
    assert hpoly(chern_projective(2)) == "1+3h+3h^{2}" and hpoly(chern_projective(3)) == "1+4h+6h^{2}+4h^{3}"
    for m in (3, 4):
        alt = poly_sum([{e: (-1) ** k * v for e, v in elementary_e(k, m).items()} for k in range(1, m + 1)]
                       + [{(0,) * m: 1}])
        assert one_minus_product(m) == {e: v for e, v in alt.items() if v}
    assert poly_str(elementary_e(2, 3)) == "x_1x_2+x_1x_3+x_2x_3"
    mons = staircase_monomials(3)
    assert len(mons) == factorial(3) == 6 and set(mons) == {(a, b, 0) for a in range(3) for b in range(2)}
    assert divided_difference({(1, 0, 0): 1}, 1) == {(0, 0, 0): 1}
    assert not any(divided_difference({(0, 0, 0): 1}, 1).values())


# ---------------------------------------------------------------- 1. 問題與工具
def part_tools(scene):
    q = tex(r"H^*(Fl(m))=\mathbb Z[x_1,\dots,x_m]/(e_1,\dots,e_m)", 40).move_to(np.array([0, 2.5, 0]))
    base = Line(np.array([-6.2, -1.6, 0]), np.array([-2.4, -1.6, 0])).set_stroke(WHITE, 3)
    fibres = VGroup(*[Line(np.array([x, -2.3, 0]), np.array([x, 0.1, 0])) for x in np.linspace(-5.9, -2.7, 9)])
    fibres.set_stroke(TEAL, 3)
    xl = tex("X", 32).next_to(base, RIGHT, buff=0.15)
    ll = tex("L", 32, TEAL).next_to(fibres, UP, buff=0.15)
    rows = VGroup(tex(r"c(L)=1+c_1(L)", 36),
                  tex(r"c(E\oplus F)=c(E)\,c(F)", 36, YELLOW),
                  tex(r"c(E)=\prod_{i}(1+\alpha_i),\quad c_k(E)=e_k(\alpha)", 36))
    rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(np.array([2.3, -0.75, 0]))
    tags = VGroup(zh("線叢", font_size=24, color=MUTED_COLOR), zh("Whitney (14)", font_size=24, color=MUTED_COLOR),
                  zh("分裂原理（Lemma 7）", font_size=24, color=MUTED_COLOR))
    for t, r in zip(tags, rows):
        t.next_to(r, UP, buff=0.08, aligned_edge=LEFT)
    assert_in_frame(q, base, fibres, xl, ll, rows, tags)
    assert_apart(q, VGroup(ll, tags), 0.15)
    assert_apart(VGroup(base, fibres, xl, ll), VGroup(rows, tags), 0.3)
    for a, b in zip(rows, tags[1:]):
        assert_apart(a, b, 0.05)

    scene.play(Write(q), run_time=1.5)
    scene.say("問：第 10 章說 ", r"$H^*(Fl(m))$", " 裡所有 ", "$e_k(x)$", " 都是 0——為什麼？", wait=SLOW * 0.6)
    scene.say("工具：向量叢的 Chern 類 ", r"$c(E)=1+c_1(E)+c_2(E)+\cdots$", wait=SLOW * 0.3)
    scene.play(ShowCreation(base), FadeIn(xl), run_time=0.7)
    scene.play(LaggedStartMap(ShowCreation, fibres, lag_ratio=0.1), FadeIn(ll), run_time=1.2)
    scene.say("線叢：每一點上放一條複直線，只有 ", "$c_1$", wait=SLOW * 0.2)
    scene.play(FadeIn(tags[0]), Write(rows[0]), run_time=1.0)
    scene.play(FadeIn(tags[1]), Write(rows[1]), run_time=1.0)
    scene.say("Whitney 公式：直和（或正合列）的 Chern 類相乘", wait=SLOW * 0.4)
    scene.play(FadeIn(tags[2]), Write(rows[2]), run_time=1.2)
    scene.say("分裂原理：計算時可以假裝 ", "$E$", " 是線叢的直和", wait=SLOW * 0.5)


# ---------------------------------------------------------------- 2. 射影空間
def part_projective(scene):
    euler = tex(r"0\to\mathbb C\to\mathbb C^{n+1}\otimes\mathcal O(1)\to T\mathbb P^n\to 0", 36).move_to(np.array([0, 2.5, 0]))
    gen = tex(r"c(T\mathbb P^n)=(1+h)^{n+1}", 40, YELLOW).move_to(np.array([0, 1.55, 0]))
    rows = VGroup()
    for k, n in enumerate((1, 2, 3)):
        c = chern_projective(n)
        lhs = tex(r"c(T\mathbb P^{%d})=(1+h)^{%d}=%s" % (n, n + 1, hpoly(c)), 34)
        rhs = tex(r"c_{%d}=%d=\chi(\mathbb P^{%d})" % (n, c[n], n), 34, OK)
        y = 0.45 - 0.95 * k
        lhs.move_to(np.array([-1.0, y, 0]), aligned_edge=RIGHT).shift(1.2 * RIGHT)
        rhs.move_to(np.array([1.0, y, 0]), aligned_edge=LEFT).shift(1.0 * RIGHT)
        rows.add(VGroup(lhs, rhs))
    assert_in_frame(euler, gen, rows)
    assert_apart(euler, gen, 0.1)
    assert_apart(gen, rows, 0.15)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a, b, 0.15)
    for r in rows:
        assert_apart(r[0], r[1], 0.3)

    scene.say("例：射影空間的切叢，用 Euler 正合列", wait=SLOW * 0.2)
    scene.play(Write(euler), run_time=1.5)
    scene.play(Write(gen), run_time=1.0)
    scene.say("Whitney：", r"$c(T\mathbb P^n)=c(\mathcal O(1))^{n+1}=(1+h)^{n+1}$", "，截到 ", "$h^n$", wait=SLOW * 0.5)
    for k in range(3):
        scene.play(FadeIn(rows[k][0]), run_time=0.8)
        scene.play(FadeIn(rows[k][1], shift=0.2 * LEFT), run_time=0.7)
        if k == 1:
            scene.say(r"$\mathbb P^2$", "：", r"$1+3h+3h^2$", "，頂端的 ", "$c_2=3$", "＝三個胞腔＝", r"$\chi(\mathbb P^2)$", wait=SLOW * 0.5)
    scene.say(r"$\mathbb P^3$", "：", "$c_3=4$", "；頂端的 Chern 類就是 Euler 示性數", wait=SLOW * 0.6)


# ---------------------------------------------------------------- 3. 旗流形：e_k = 0
def part_flag(scene):
    seg = 1.15
    bars, labels = VGroup(), VGroup()
    names = [r"U_1", r"U_2", r"U_3=\mathbb C^3"]
    for i in range(3):
        y = 1.4 - 1.0 * i
        row = VGroup()
        for j in range(i + 1):
            r = Rectangle(width=seg, height=0.6).set_fill(L_COLORS[j], 0.55).set_stroke(WHITE, 2)
            r.move_to(np.array([-4.4 + (j + 0.5) * seg, y, 0]))
            t = tex("L_%d" % (j + 1), 28).move_to(r.get_center())
            row.add(VGroup(r, t))
        bars.add(row)
        labels.add(tex(names[i], 30, MUTED_COLOR).next_to(row, LEFT, buff=0.2).align_to(np.array([-4.6, 0, 0]), RIGHT))
    eqs = VGroup(tex(r"L_i=U_i/U_{i-1},\qquad x_i=-c_1(L_i)", 32),
                 tex(r"c(\mathbb C^3)=c(L_1)\,c(L_2)\,c(L_3)", 32),
                 tex(r"1=(1-x_1)(1-x_2)(1-x_3)", 32, YELLOW),
                 tex(r"=1-e_1+e_2-e_3", 32, YELLOW),
                 tex(r"\Rightarrow\ e_1=e_2=e_3=0", 36, OK))
    eqs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([2.9, 0.3, 0]))
    eqs[3].shift(0.5 * RIGHT)
    gen = tex(r"\prod_{i=1}^m(1-x_i)=1\ \Rightarrow\ e_1=\cdots=e_m=0", 34, OK).move_to(np.array([0, -2.5, 0]))
    assert_in_frame(bars, labels, eqs, gen)
    assert_apart(VGroup(bars, labels), eqs, 0.3)
    assert_apart(eqs, gen, 0.15)
    assert_apart(VGroup(bars, labels), gen, 0.15)

    scene.say("旗流形上：每一點是一個旗 ", r"$U_1\subset U_2\subset\mathbb C^3$", wait=SLOW * 0.3)
    for i in range(3):
        scene.play(FadeIn(labels[i]), LaggedStartMap(FadeIn, bars[i], lag_ratio=0.3), run_time=0.9)
    scene.say("平凡叢 ", r"$\mathbb C^3$", " 被一層層切開：", r"$L_i=U_i/U_{i-1}$", " 是線叢", wait=SLOW * 0.3)
    scene.play(Write(eqs[0]), run_time=1.0)
    scene.say("第 10 章的變數：", r"$x_i=-c_1(L_i)$", wait=SLOW * 0.3)
    scene.play(Write(eqs[1]), run_time=1.0)
    scene.say("Whitney 公式把三層乘起來；平凡叢的 Chern 類是 1", wait=SLOW * 0.3)
    scene.play(Write(eqs[2]), run_time=1.0)
    scene.play(Write(eqs[3]), run_time=1.0)
    scene.say("展開：", "$e_k$", " 是第 ", "$k$", " 次的部分", wait=SLOW * 0.3)
    scene.play(Write(eqs[4]), run_time=0.9)
    scene.say("各次數分別比較：", "$e_1=e_2=e_3=0$", wait=SLOW * 0.4)
    scene.play(FadeIn(gen, shift=0.2 * UP), run_time=0.8)
    scene.say("對任何 ", "$m$", " 都一樣：這就是 ", "$e_k(x)=0$", " 的原因", wait=SLOW * 0.5)


# ---------------------------------------------------------------- 4. 射影叢與基底
def part_basis(scene):
    pb = tex(r"H^*(\mathbb P(E))=H^*(X)[\zeta]/(\zeta^e+c_1\zeta^{e-1}+\cdots+c_e)", 36, YELLOW).move_to(np.array([0, 2.6, 0]))
    tw = VGroup(tex(r"Fl(3)", 34), tex(r"\mathbb P^2", 34), tex(r"\mathrm{pt}", 34))
    for k, m in enumerate(tw):
        m.move_to(np.array([-5.0, 1.3 - 1.45 * k, 0]))
    arrows = VGroup()
    for k, (fib, gen) in enumerate(((r"\mathbb P^1", r"x_2"), (r"\mathbb P^2", r"x_1"))):
        a = Arrow(tw[k].get_bottom(), tw[k + 1].get_top(), buff=0.12).set_color(GREY_B)
        lab = tex(r"%s:\ %s" % (fib, gen), 28, L_COLORS[1 - k]).next_to(a, RIGHT, buff=0.15)
        arrows.add(VGroup(a, lab))
    mons = staircase_monomials(3)
    grid = VGroup()
    for b in range(2):
        for a in range(3):
            assert (a, b, 0) in mons
            grid.add(tex(mono_tex((a, b, 0)), 36).move_to(np.array([0.4 + 1.5 * a, 1.0 - 0.9 * b, 0])))
    gl = tex(r"x^I,\ i_j\le m-j", 30, MUTED_COLOR).next_to(grid, RIGHT, buff=0.5)
    lem = tex(r"p_*(\zeta^{e-1})=1", 36, OK).move_to(np.array([-0.2, -1.35, 0]))
    dd = tex(r"\partial_1(x_1)=1,\qquad \partial_1(1)=0", 34, OK).next_to(lem, RIGHT, buff=0.8)
    assert_in_frame(pb, tw, arrows, grid, gl, lem, dd)
    assert_apart(pb, VGroup(tw, grid), 0.15)
    assert_apart(VGroup(tw, arrows), VGroup(grid, gl, lem, dd), 0.3)
    assert_apart(grid, VGroup(lem, dd), 0.2)

    scene.say("另一個公式：射影叢 (33)", wait=SLOW * 0.2)
    scene.play(Write(pb), run_time=1.6)
    scene.say(r"$H^*(\mathbb P(E))$", " 是 ", r"$H^*(X)$", " 上以 ", r"$1,\zeta,\dots,\zeta^{e-1}$", " 為基底的自由模", wait=SLOW * 0.4)
    scene.play(FadeIn(tw[0]), run_time=0.5)
    for k in range(2):
        scene.play(GrowArrow(arrows[k][0]), FadeIn(arrows[k][1]), FadeIn(tw[k + 1]), run_time=0.9)
    scene.say(r"$Fl(3)$", " 是一串射影叢：先選直線（", r"$\mathbb P^2$", "），再選平面（", r"$\mathbb P^1$", "）", wait=SLOW * 0.4)
    scene.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.15), run_time=1.5)
    scene.play(FadeIn(gl), run_time=0.6)
    scene.say("每層貢獻 ", r"$1,\dots,\zeta^{e-1}$", "：得到命題 3 的基底，共 ", "$3!=6$", " 個", wait=SLOW * 0.5)
    scene.play(Write(lem), run_time=1.0)
    scene.say("Lemma 9：沿著射影叢推下去，", r"$\zeta^{e-1}\mapsto1$", "，較低的次方 ", r"$\mapsto0$", wait=SLOW * 0.4)
    scene.play(Write(dd), run_time=1.0)
    scene.say("對 ", r"$\mathbb P^1$", " 叢 ", "$(e=2)$", "：這正是差商 ", r"$\partial_i$", " 的幾何", wait=SLOW * 0.5)
    scene.say("收束：一條 Whitney 公式解釋了整個 Borel 表示", wait=SLOW * 0.7)


class SceneF64ChernClasses(ChuScene):
    def construct(self):
        self.show_header("Chern 類：基本對稱多項式為什麼是 0")
        check_math()
        part_tools(self)
        self.clear_stage()
        part_projective(self)
        self.clear_stage()
        part_flag(self)
        self.clear_stage()
        part_basis(self)
        self.wait(1.0)
