"""
Scene F62 —— 數格子就是數洞：胞腔給出同調（Fulton 附錄 B，§B.1–B.3 Lemma 6，書 p.211–222）
執行（在 codes/ 內）：manimgl scenes/sceneF62_cells_homology.py SceneF62CellsHomology
"""
import sys
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import betti_from_cells
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.scene_base import ChuScene
from utils.schubert import (count_flags_F2, count_subspaces_F2, flag_cell_pattern, gaussian_binomial,
                            grass_cell_pattern, length, perms, q_factorial)
from utils.schubert_draw import CellMatrixMob
from utils.styles import MUTED_COLOR, mixed, zh

SLOW = 6.0
OK = "#7CE38B"
BAR = TEAL
STEP = 1.2
BOX24 = [(), (1,), (2,), (1, 1), (2, 1), (2, 2)]


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def stars(p):
    return sum(row.count("*") for row in p)


def by_dim(patterns):
    out = {}
    for p in patterns:
        out.setdefault(stars(p), []).append(p)
    return [out.get(d, []) for d in range(max(out) + 1)]


P2_CELLS = [grass_cell_pattern((k,), 1, 2) for k in (2, 1, 0)]
GR_CELLS = [grass_cell_pattern(lam, 2, 2) for lam in BOX24]
FL_CELLS = [flag_cell_pattern(w) for w in perms(3)]


def qpoly(coeffs, var, step=1):
    terms = []
    for k, c in enumerate(coeffs):
        if not c:
            continue
        e = k * step
        mono = "" if e == 0 else var if e == 1 else "%s^{%d}" % (var, e)
        terms.append((str(c) if c != 1 or not mono else "") + mono)
    return "+".join(terms)


def check_math():
    assert [len(g) for g in by_dim(P2_CELLS)] == [1, 1, 1]
    assert betti_from_cells([1, 1, 1]) == ([1, 0, 1, 0, 1], 3)
    gr = [len(g) for g in by_dim(GR_CELLS)]
    assert gr == [1, 1, 2, 1, 1] == gaussian_binomial(4, 2)
    assert [stars(grass_cell_pattern(lam, 2, 2)) for lam in BOX24] == [4 - sum(lam) for lam in BOX24]
    assert betti_from_cells(gr) == ([1, 0, 1, 0, 2, 0, 1, 0, 1], 6) and comb(4, 2) == 6
    assert all(sum(r.count("1") for r in p) == 2 for p in GR_CELLS)            # 每個胞腔一個座標平面
    assert len({tuple(r.index("1") for r in p) for p in GR_CELLS}) == 6
    fl = [len(g) for g in by_dim(FL_CELLS)]
    assert all(stars(flag_cell_pattern(w)) == length(w) for w in perms(3))
    assert fl == [1, 2, 2, 1] == q_factorial(3)
    assert betti_from_cells(fl) == ([1, 0, 2, 0, 2, 0, 1], 6) and factorial(3) == 6
    for cnt in ([1, 1, 1], gr, fl):                                             # Poincaré 對偶
        b, _ = betti_from_cells(cnt)
        assert b == b[::-1]
    assert count_subspaces_F2(4, 2) == sum(c * 2 ** k for k, c in enumerate(gr)) == 35
    assert count_flags_F2(3) == sum(c * 2 ** k for k, c in enumerate(fl)) == 21
    assert qpoly(gr, "q") == "1+q+2q^{2}+q^{3}+q^{4}" and qpoly(gr, "t", 2) == "1+t^{2}+2t^{4}+t^{6}+t^{8}"


def sphere(r=1.0):
    ball = Circle(radius=r).set_fill(BLUE_E, 0.55).set_stroke(BLUE_B, 3)
    eq = DashedVMobject(Ellipse(width=2 * r, height=0.42 * r), num_dashes=26).set_stroke(BLUE_B, 2)
    return VGroup(ball, eq)


def betti_bars(b, y_axis, unit=0.5, w=0.6):
    n = len(b)
    x0 = -(n - 1) * STEP / 2
    bars, vals, idx = VGroup(), VGroup(), VGroup()
    for i, v in enumerate(b):
        x = x0 + i * STEP
        if v:
            r = Rectangle(width=w, height=v * unit).set_fill(BAR, 0.75).set_stroke(WHITE, 1.5)
            r.move_to(np.array([x, y_axis + v * unit / 2, 0]))
        else:
            r = Line(np.array([x - w / 2, y_axis, 0]), np.array([x + w / 2, y_axis, 0])).set_stroke(GREY_C, 4)
        bars.add(r)
        vals.add(tex(str(v), 30, WHITE if v else MUTED_COLOR).move_to(np.array([x, y_axis + v * unit + 0.25, 0])))
        idx.add(tex("b_{%d}" % i, 26, MUTED_COLOR).move_to(np.array([x, y_axis - 0.32, 0])))
    axis = Line(np.array([x0 - 0.55, y_axis, 0]), np.array([-x0 + 0.55, y_axis, 0])).set_stroke(GREY_B, 2)
    return VGroup(axis, bars, vals, idx)


def cell_columns(groups, nbars, cs, y_mat, y_lab):
    x0 = -(nbars - 1) * STEP / 2
    cols, labs = VGroup(), VGroup()
    for d, g in enumerate(groups):
        x = x0 + 2 * d * STEP
        stack = VGroup(*[CellMatrixMob(p, cs=cs) for p in g]).arrange(DOWN, buff=0.2).move_to(np.array([x, y_mat, 0]))
        cols.add(stack)
        labs.add(tex(r"\mathbb C^{%d}" % d, 30, MUTED_COLOR).move_to(np.array([x, y_lab, 0])))
    return cols, labs


def screen(groups, cs, y_mat, y_lab, y_axis, chi_tex):
    b, chi = betti_from_cells([len(g) for g in groups])
    cols, labs = cell_columns(groups, len(b), cs, y_mat, y_lab)
    bars = betti_bars(b, y_axis)
    chi_m = tex(chi_tex, 32, YELLOW).move_to(np.array([0, y_axis - 0.95, 0]))
    assert_in_frame(cols, labs, bars, chi_m)
    assert_apart(labs, cols, 0.08)
    assert_apart(cols, bars, 0.15)
    assert_apart(bars, chi_m, 0.1)
    return cols, labs, bars, chi_m


def count_into_bars(scene, cols, bars, run_time=0.8):
    for d, stack in enumerate(cols):
        scene.play(TransformFromCopy(stack, bars[1][2 * d]), FadeIn(bars[2][2 * d]), run_time=run_time)
    scene.play(*[FadeIn(bars[1][i]) for i in range(1, len(bars[1]), 2)],
               *[FadeIn(bars[2][i]) for i in range(1, len(bars[2]), 2)], run_time=0.7)


# ---------------------------------------------------------------- 1. 洞
def part_holes(scene):
    circ = Circle(radius=0.95).set_stroke(TEAL, 5).move_to(np.array([-4.4, 0.8, 0]))
    sph = sphere(0.95).move_to(np.array([0, 0.8, 0]))
    p1 = sphere(0.95).move_to(np.array([4.4, 0.8, 0]))
    pole = Dot(p1.get_top(), radius=0.09).set_color(YELLOW)
    c0 = tex(r"\mathbb C^0", 28, YELLOW).next_to(pole, UP, buff=0.12)
    c1 = tex(r"\mathbb C^1", 30, WHITE).move_to(p1.get_center() + 0.35 * DOWN)
    lab1 = mixed("$H_1$", "：1 維的洞", font_size=26).next_to(circ, DOWN, buff=0.4)
    lab2 = mixed("$H_2$", "：2 維的洞", font_size=26).next_to(sph, DOWN, buff=0.4)
    lab3 = tex(r"\mathbb P^1=\mathbb C^0\sqcup\mathbb C^1", 32).next_to(p1, DOWN, buff=0.4)
    b3 = tex(r"b_0=1,\ b_1=0,\ b_2=1", 30, OK).next_to(lab3, DOWN, buff=0.3)
    ck = tex(r"\mathbb C^k\cong\mathbb R^{2k}", 38, YELLOW).move_to(np.array([0, -2.35, 0]))
    assert_in_frame(circ, sph, p1, c0, c1, lab1, lab2, lab3, b3, ck)
    assert_apart(VGroup(circ, lab1), VGroup(sph, lab2), 0.3)
    assert_apart(VGroup(sph, lab2), VGroup(p1, lab3, b3), 0.3)
    assert_apart(b3, ck, 0.1)

    scene.say("問：怎麼知道 ", "$Gr(2,4)$", " 有幾個「洞」？", wait=SLOW * 0.6)
    scene.say("一句話的同調：", "$H_i$", " 量的是 ", "$i$", " 維的洞", wait=SLOW * 0.2)
    scene.play(ShowCreation(circ), run_time=1.0)
    scene.play(FadeIn(lab1), run_time=0.5)
    scene.say("圓圈圍住一個 1 維的洞：", "$b_1=1$", wait=SLOW * 0.3)
    scene.play(FadeIn(sph), run_time=0.9)
    scene.play(FadeIn(lab2), run_time=0.5)
    scene.say("球面包住一個 2 維的洞：", "$b_2=1$", "（", "$b_i$", " 是 Betti 數）", wait=SLOW * 0.4)
    scene.say("複數的空間：", r"$\mathbb C^k$", " 是 ", "$2k$", " 維的實空間", wait=SLOW * 0.3)
    scene.play(FadeIn(p1), run_time=0.8)
    scene.play(FadeIn(pole), Write(c0), Write(c1), run_time=0.9)
    scene.play(Write(lab3), run_time=0.8)
    scene.say("射影直線 ", r"$\mathbb P^1$", "＝一個點加上一個平面 ", r"$\mathbb C$", "：正是球面", wait=SLOW * 0.4)
    scene.play(FadeIn(b3), run_time=0.6)
    scene.play(Write(ck), run_time=1.0)
    scene.say("Lemma 6 證明的開頭：一塊 ", r"$\mathbb C^k$", " 胞腔只貢獻在 ", "$H_{2k}$", wait=SLOW * 0.6)


# ---------------------------------------------------------------- 2. Lemma 6 與 P^2
def part_lemma(scene):
    lem = mixed("Lemma 6：空間切成胞腔 ", r"$\mathbb C^{n_{ij}}$", r"$\Rightarrow$", "胞腔閉包的類是同調的基底，奇數維的同調是 0",
                font_size=26)
    box = SurroundingRectangle(lem, buff=0.18).set_stroke(YELLOW, 2)
    top = VGroup(box, lem).move_to(np.array([0, 2.75, 0]))
    cols, labs, bars, chi = screen(by_dim(P2_CELLS), 0.4, 1.15, 1.85, -1.2, r"\chi(\mathbb P^2)=1+1+1=3")
    assert_in_frame(top)
    assert_apart(top, labs, 0.1)

    scene.say("Lemma 6 把這件事推廣到整個空間", wait=SLOW * 0.2)
    scene.play(FadeIn(top), run_time=1.0)
    scene.wait(SLOW * 0.6)
    scene.say("例：", r"$\mathbb P^2$", " 切成點、直線、平面：列梯形矩陣，星號是自由座標", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(FadeIn, cols, lag_ratio=0.3), FadeIn(labs), run_time=1.5)
    scene.play(*[Indicate(c.stars(), color=YELLOW) for stack in cols for c in stack if len(c.stars())], run_time=1.0)
    scene.say("星號數 ", "$0,1,2$", " 就是胞腔的複維數", wait=SLOW * 0.4)
    scene.play(ShowCreation(bars[0]), FadeIn(bars[3]), run_time=0.8)
    count_into_bars(scene, cols, bars)
    scene.say("Betti 數 ", r"$1,0,1,0,1$", "：奇數維全是 0", wait=SLOW * 0.4)
    scene.play(Write(chi), run_time=0.9)
    scene.say("Euler 示性數 ", r"$\chi=\sum(-1)^ib_i$", " 就是胞腔的個數", wait=SLOW * 0.6)


# ---------------------------------------------------------------- 3. Gr(2,4) 與 Fl(3)
def part_grass(scene):
    cols, labs, bars, chi = screen(by_dim(GR_CELLS), 0.3, 1.75, 2.75, -1.25, r"\chi(Gr(2,4))=1+1+2+1+1=6")
    mid = DashedLine(np.array([0, -1.45, 0]), np.array([0, 0.35, 0])).set_stroke(GREY_B, 2)

    scene.say(r"$Gr(2,4)$", "：六個胞腔，星號數就是複維數（第 9 章）", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(FadeIn, cols, lag_ratio=0.2), FadeIn(labs), run_time=1.8)
    scene.say("維數 ", "$0,1,2,3,4$", " 的胞腔各有 ", "$1,1,2,1,1$", " 個", wait=SLOW * 0.4)
    scene.play(ShowCreation(bars[0]), FadeIn(bars[3]), run_time=0.8)
    count_into_bars(scene, cols, bars, run_time=0.7)
    scene.say("Lemma 6 ", r"$\Rightarrow$", " ", r"$b_0,\dots,b_8=1,0,1,0,2,0,1,0,1$", wait=SLOW * 0.5)
    scene.play(Write(chi), run_time=0.9)
    scene.play(*[Indicate(c.ones(), color=OK) for stack in cols for c in stack], run_time=1.2)
    scene.say(r"$\chi=6$", "＝不動點個數：每個胞腔恰含一個座標平面（1 的位置）", wait=SLOW * 0.7)
    scene.play(ShowCreation(mid), run_time=0.6)
    for i in range(4):
        scene.play(Indicate(VGroup(bars[1][i], bars[1][8 - i]), color=YELLOW), run_time=0.45)
    scene.say("Poincaré 對偶：", r"$b_i=b_{8-i}$", "，左右對稱", wait=SLOW * 0.5)


def part_flag(scene):
    cols, labs, bars, chi = screen(by_dim(FL_CELLS), 0.28, 1.45, 2.75, -1.25, r"\chi(Fl(3))=1+2+2+1=6=3!")
    scene.say("旗流形 ", "$Fl(3)$", "：", "$3!=6$", " 個胞腔，星號數 ", r"$=\ell(w)$", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(FadeIn, cols, lag_ratio=0.2), FadeIn(labs), run_time=1.8)
    scene.play(ShowCreation(bars[0]), FadeIn(bars[3]), run_time=0.8)
    count_into_bars(scene, cols, bars, run_time=0.7)
    scene.play(Write(chi), run_time=0.9)
    scene.say(r"$1,2,2,1$", " 個胞腔 ", r"$\Rightarrow$", " ", r"$b=1,0,2,0,2,0,1$", "，又是左右對稱", wait=SLOW * 0.7)


# ---------------------------------------------------------------- 4. 對照 F_q 的點數
def part_fq(scene):
    gr, fl = gaussian_binomial(4, 2), q_factorial(3)
    rows = VGroup(
        tex(r"\#Gr(2,4)(\mathbb F_q)=" + qpoly(gr, "q"), 36),
        tex(r"P_{Gr(2,4)}(t)=" + qpoly(gr, "t", 2), 36, BAR),
        tex(r"\#Fl(3)(\mathbb F_q)=" + qpoly(fl, "q"), 36),
        tex(r"P_{Fl(3)}(t)=" + qpoly(fl, "t", 2), 36, BAR),
    )
    for k, y in enumerate((2.2, 1.0, -0.35, -1.55)):
        rows[k].move_to(np.array([-0.6, y, 0]))
    arrows = VGroup()
    for k in (0, 2):
        a = Arrow(rows[k].get_bottom() + 0.05 * DOWN, rows[k + 1].get_top() + 0.05 * UP, buff=0).set_color(GREY_B)
        lab = tex(r"q\mapsto t^2", 28, YELLOW).next_to(a, RIGHT, buff=0.15)
        arrows.add(VGroup(a, lab))
    notes = VGroup(tex(r"q=2:\ 35", 28, MUTED_COLOR).move_to(np.array([5.3, 2.2, 0])),
                   tex(r"q=2:\ 21", 28, MUTED_COLOR).move_to(np.array([5.3, -0.35, 0])))
    end = zh("星號數決定一切", font_size=34, color=OK).move_to(np.array([0, -2.5, 0]))
    assert_in_frame(rows, arrows, notes, end)
    assert_apart(rows[0], notes[0], 0.2)
    assert_apart(rows[2], notes[1], 0.2)
    assert_apart(rows[3], end, 0.15)

    scene.say("再對照第 9、10 章數過的 ", r"$\mathbb F_q$", " 上的點數", wait=SLOW * 0.2)
    scene.play(Write(rows[0]), run_time=1.2)
    scene.play(FadeIn(notes[0]), run_time=0.5)
    scene.say("有限域上數子空間：", "$q^k$", " 的係數就是 ", "$k$", " 維胞腔的個數", wait=SLOW * 0.4)
    scene.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), run_time=0.8)
    scene.play(TransformFromCopy(rows[0], rows[1]), run_time=1.2)
    scene.say("把 ", "$q$", " 換成 ", "$t^2$", "：就是 Poincaré 多項式 ", r"$\sum b_it^i$", wait=SLOW * 0.5)
    scene.play(Write(rows[2]), FadeIn(notes[1]), run_time=1.2)
    scene.play(GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), run_time=0.8)
    scene.play(TransformFromCopy(rows[2], rows[3]), run_time=1.2)
    scene.say("旗流形也一樣：", r"$(1+q)(1+q+q^2)$", " 變成 ", r"$1+2t^2+2t^4+t^6$", wait=SLOW * 0.5)
    scene.play(FadeIn(end, shift=0.2 * UP), run_time=0.8)
    scene.say("收束：星號數決定一切", wait=SLOW * 0.6)


class SceneF62CellsHomology(ChuScene):
    def construct(self):
        self.show_header("數格子就是數洞：胞腔給出同調")
        check_math()
        part_holes(self)
        self.clear_stage()
        part_lemma(self)
        self.clear_stage()
        part_grass(self)
        self.clear_stage()
        part_flag(self)
        self.clear_stage()
        part_fq(self)
        self.wait(1.0)
