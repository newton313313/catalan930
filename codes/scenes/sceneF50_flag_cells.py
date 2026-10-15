"""
Scene F50 —— 旗流形：m! 個不動點與星號（Fulton §10.1–10.2，書 p.154–162）
執行（在 codes/ 內）：manimgl scenes/sceneF50_flag_cells.py SceneF50FlagCells

Fl(3) 裡被對角矩陣固定的旗 = (座標三角形的頂點, 過它的邊)：3×2 = 6 = 3!，標成置換 w（Lemma 2）；
胞腔 X°_w：第 p 列在第 w(p) 行放 1，右邊與下方是 0，其餘星號，星號數 = ℓ(w)：S_3 是 0,1,1,2,2,3；書上 426135 有 7 顆；
[3]_q! = 1+2q+2q²+q³，q=2 → 21（Fano 平面：7 點 × 3 線）；S_4 各層 1,3,5,6,5,3,1，q=2 → 315；
σ_w = [Ω_w] = [X_{w0 w}]，餘維 ℓ(w)；對偶 ⟨σ_u, σ_{w0 v}⟩ = δ_uv（式 (2)）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *
from itertools import combinations
from math import factorial

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR
from utils.scene_base import ChuScene
from utils.schubert import (bruhat_levels, count_flags_F2, flag_cell_pattern, inversions, lehmer_code, length,
                            perm_str, q_factorial)
from utils.schubert_draw import STAR_COLOR, ZERO_COLOR, CellMatrixMob
from utils.styles import MUTED_COLOR, mixed, zh

W3 = [(1, 2, 3), (2, 1, 3), (1, 3, 2), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
EX = (2, 3, 1)
BOOK = (4, 2, 6, 1, 3, 5)
S4_LEVELS = [1, 3, 5, 6, 5, 3, 1]
SLOW = 3.8


def stars(pattern):
    return sum(row.count("*") for row in pattern)


def w0_times(u):
    m = len(u)
    return tuple(m + 1 - x for x in u)


def fit(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def tri_points(center, size):
    c = np.array((tuple(center) + (0.0, 0.0, 0.0))[:3], dtype=float)
    return {1: c + size * np.array([0, 0.45, 0]), 2: c + size * np.array([-0.55, -0.4, 0]),
            3: c + size * np.array([0.55, -0.4, 0])}


def flag_tri(w, center, size=1.0):
    """座標三角形上的不動旗：點 e_{w(1)}（黃點）、線 ⟨e_{w(1)}, e_{w(2)}⟩（青色粗邊）。"""
    P = tri_points(center, size)
    edges = VGroup(Line(P[1], P[2]), Line(P[2], P[3]), Line(P[1], P[3])).set_stroke(GREY_C, 1.5)
    hl = Line(P[w[0]], P[w[1]]).set_stroke(TEAL_B, 5)
    dot = Dot(P[w[0]], radius=0.08).set_color(OP_COLOR)
    return VGroup(edges, hl, dot)


def fano_data():
    """F_2^3 的非零向量（位元表示 1..7）＝ 7 個點；2 維子空間 {a, b, a^b} ＝ 7 條線。"""
    pts = list(range(1, 8))
    lines = sorted({frozenset((a, b, a ^ b)) for a, b in combinations(pts, 2)}, key=sorted)
    return pts, lines


def check_math():
    assert [length(w) for w in W3] == [0, 1, 1, 2, 2, 3] and sorted(W3) == sorted(tuple(p) for l in bruhat_levels(3)
                                                                                for p in l)
    for w in W3:
        assert stars(flag_cell_pattern(w)) == length(w)
    flags = {(w[0], frozenset(w[:2])) for w in W3}             # (頂點, 過它的邊)
    assert len(flags) == 3 * 2 == factorial(3) == len(W3)
    assert flag_cell_pattern(EX) == [["*", "1", "0"], ["*", "0", "1"], ["1", "0", "0"]]
    assert inversions(EX) == [(1, 3), (2, 3)] and length(EX) == 2
    assert [row.index("1") + 1 for row in flag_cell_pattern(EX)] == list(EX)
    pb = flag_cell_pattern(BOOK)
    assert [row.count("*") for row in pb] == list(lehmer_code(BOOK)) == [3, 1, 3, 0, 0, 0]
    assert stars(pb) == length(BOOK) == 7 and perm_str(BOOK) == "426135"
    assert q_factorial(3) == [1, 2, 2, 1] == [len(l) for l in bruhat_levels(3)]
    assert sum(c * 2 ** k for k, c in enumerate(q_factorial(3))) == 21 == count_flags_F2(3) == 7 * 3
    assert [c * 2 ** k for k, c in enumerate(q_factorial(3))] == [1, 4, 8, 8]
    assert q_factorial(4) == S4_LEVELS == [len(l) for l in bruhat_levels(4)]
    assert [c * 2 ** k for k, c in enumerate(S4_LEVELS)] == [1, 6, 20, 48, 80, 96, 64]
    assert sum(c * 2 ** k for k, c in enumerate(S4_LEVELS)) == 315 == 1 * 3 * 7 * 15 == count_flags_F2(4)
    pts, lines = fano_data()
    assert len(pts) == 7 and len(lines) == 7 and all(sum(p in l for l in lines) == 3 for p in pts)
    assert [(perm_str(u), perm_str(w0_times(u))) for u in W3[:3]] == [("123", "321"), ("213", "231"), ("132", "312")]
    assert all(length(u) + length(w0_times(u)) == 3 for u in W3)


# ---------------------------------------------------------------- 1. 座標三角形與不動的旗
def part_fixed(scene):
    P = tri_points((-4.0, 0.35), 3.6)
    big = VGroup(Line(P[1], P[2]), Line(P[2], P[3]), Line(P[1], P[3])).set_stroke(GREY_B, 2.5)
    vdots = VGroup(*[Dot(P[k], radius=0.09).set_color(WHITE) for k in (1, 2, 3)])
    vlabs = VGroup(Tex("e_1", font_size=32).next_to(P[1], UP, buff=0.15),
                   Tex("e_2", font_size=32).next_to(P[2], DL, buff=0.1),
                   Tex("e_3", font_size=32).next_to(P[3], DR, buff=0.1))
    act = Tex(r"t\cdot[x_1:x_2:x_3]=[t_1x_1:t_2x_2:t_3x_3]", font_size=30).move_to(np.array([-4.0, -1.85, 0]))

    def bary(a, b, c):
        return a * P[1] + b * P[2] + c * P[3]

    gen = Dot(bary(0.3, 0.3, 0.4), radius=0.08).set_color(NEG_COLOR)
    cnt = Tex(r"3\times2=6=3!", font_size=40).set_color(POS_COLOR).move_to(np.array([3.6, 2.45, 0]))
    minis, labs = [], []
    for k, w in enumerate(W3):
        c = np.array([1.6 + 2.0 * (k % 3), 1.05 - 2.1 * (k // 3), 0])
        minis.append(flag_tri(w, c, 1.1))
        labs.append(Tex(perm_str(w), font_size=30).next_to(minis[-1], DOWN, buff=0.2))
    left = VGroup(big, vdots, vlabs, act)
    right = VGroup(cnt, *minis, *labs)
    assert_in_frame(left, right)
    assert_apart(left, right, 0.4)
    assert_apart(cnt, minis[1], 0.2)
    assert_apart(VGroup(*labs[:3]), VGroup(*minis[3:]), 0.15)

    scene.say("問：", "$Fl(3)$", "（點在線上）裡，有幾個旗不會被對角矩陣移動？", wait=SLOW * 0.8)
    scene.play(ShowCreation(big), FadeIn(vdots), FadeIn(vlabs), run_time=1.2)
    scene.say("把 ", "$\\mathbb P^2$", " 畫成座標三角形：頂點是三個座標點 ", "$e_1,e_2,e_3$", wait=SLOW * 0.6)
    scene.play(FadeIn(act), FadeIn(gen, scale=0.5), run_time=0.9)
    scene.say("對角矩陣把每個座標各乘一個數：一般的點會被推著走", wait=SLOW * 0.2)
    for abc in ((0.5, 0.2, 0.3), (0.2, 0.55, 0.25), (0.3, 0.3, 0.4)):
        scene.play(gen.animate.move_to(bary(*abc)), run_time=0.9)
    scene.play(*[Flash(d, color=OP_COLOR) for d in vdots], run_time=1.0)
    scene.say("不動的點只有三個頂點；不動的線只有三條邊", wait=SLOW * 0.8)
    scene.say("不動的旗 ＝（一個頂點，過它的一條邊）", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(VGroup(m, l)) for m, l in zip(minis, labs)], lag_ratio=0.2), run_time=2.0)
    scene.play(Write(cnt), run_time=0.9)
    scene.say("三個頂點、每個頂點兩條邊：", "$3\\times2=6=3!$", wait=SLOW * 0.7)
    scene.say("用置換 ", "$w$", " 命名：點是 ", "$e_{w(1)}$", "，線是 ", "$\\langle e_{w(1)},e_{w(2)}\\rangle$",
              wait=SLOW * 0.9)
    scene.play(Indicate(VGroup(minis[3], labs[3]), color=OP_COLOR), run_time=1.0)
    scene.say("例如 ", "$231$", "：點 ", "$e_2$", "，線 ", "$\\langle e_2,e_3\\rangle$", wait=SLOW * 0.7)
    scene.say("Lemma 2：", "$Fl(m)$", " 的不動點正好 ", "$m!$", " 個，一個置換一個", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 2. 一個胞腔放大看
def part_cell(scene):
    pat = flag_cell_pattern(EX)
    mat = CellMatrixMob(pat, cs=0.7).move_to(np.array([-3.6, 0.5, 0]))
    wl = Tex(r"w=231", font_size=40).next_to(mat, UP, buff=0.65)
    cols = VGroup(*[Tex(str(j + 1), font_size=24).set_color(MUTED_COLOR).next_to(mat.cell(0, j), UP, buff=0.3)
                    for j in range(3)])
    rows = VGroup(*[Tex("p=%d" % (i + 1), font_size=26).set_color(MUTED_COLOR).next_to(mat, LEFT, buff=0.3)
                    .set_y(mat.cell(i, 0).get_y()) for i in range(3)])
    rules = [mixed("第 ", "$p$", " 列：在第 ", "$w(p)$", " 行放 1", font_size=26),
             mixed("1 的右邊、1 的下方：0", font_size=26),
             mixed("其餘：星號（任意複數）", font_size=26, color=STAR_COLOR)]
    for k, r in enumerate(rules):
        r.move_to(np.array([2.6, 1.7 - 0.7 * k, 0]))
    ell = Tex(r"\ell(231)=\#\{i<j:w(i)>w(j)\}=2", font_size=32).set_color(OP_COLOR).move_to(np.array([2.6, -0.55, 0]))
    zeros = VGroup(*[Tex("0", font_size=42).set_color(ZERO_COLOR).move_to(s) for s in mat.stars()])
    flag = Tex(r"\langle e_2\rangle\subset\langle e_2,e_3\rangle", font_size=36).set_color(TEAL_B)
    flag.move_to(np.array([2.6, -1.6, 0]))
    assert_in_frame(mat, wl, cols, rows, *rules, ell, flag)
    assert_apart(VGroup(mat, rows, cols), VGroup(*rules, ell, flag), 0.4)
    for u, v in zip(rules + [ell], rules[1:] + [ell, flag]):
        assert_apart(u, v, 0.1)
    assert_apart(wl, cols, 0.1)

    scene.say("每個旗也有唯一的列梯形矩陣：胞腔 ", "$X^\\circ_w$", wait=SLOW * 0.2)
    scene.play(FadeIn(wl), FadeIn(mat), FadeIn(cols), FadeIn(rows), run_time=1.0)
    for k, r in enumerate(rules):
        scene.play(FadeIn(r, shift=0.2 * LEFT), run_time=0.6)
        if k == 0:
            scene.play(Indicate(mat.ones(), color=OP_COLOR), run_time=0.9)
        elif k == 2:
            scene.play(LaggedStart(*[Flash(s, color=STAR_COLOR) for s in mat.stars()], lag_ratio=0.3), run_time=1.0)
        scene.wait(SLOW * 0.3)
    scene.say("$w=231$", "：1 依序在第 2、3、1 行；星號 2 顆", wait=SLOW * 0.6)
    scene.play(Write(ell), run_time=1.0)
    scene.say("星號數 ＝ 逆序數 ", "$\\ell(w)$", "：", "$2>1$", "、", "$3>1$", wait=SLOW * 0.8)
    scene.play(*[ReplacementTransform(s.copy(), z) for s, z in zip(mat.stars(), zeros)],
               *[s.animate.set_opacity(0) for s in mat.stars()], run_time=0.9)
    scene.play(FadeIn(flag, shift=0.2 * UP), run_time=0.8)
    scene.say("星號全填 0：三列是 ", "$e_2,e_3,e_1$", "，回到不動的旗 ", "$231$", wait=SLOW * 0.9)
    scene.say("所以 ", "$X^\\circ_w\\cong\\mathbb C^{\\ell(w)}$", "，中心就是不動點 ", "$w$", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 3. 六個胞腔、書上的例子
def part_six(scene):
    panels, ells = [], []
    for k, w in enumerate(W3):
        c = np.array([-4.4 + 4.4 * (k % 3), 1.45 - 2.4 * (k // 3), 0])
        tri = flag_tri(w, c + 0.85 * LEFT, 1.0)
        mat = CellMatrixMob(flag_cell_pattern(w), cs=0.36).move_to(c + 0.75 * RIGHT)
        lab = Tex("w=" + perm_str(w), font_size=28).move_to(c + 0.95 * UP)
        panels.append(VGroup(lab, tri, mat))
        ells.append(Tex(r"\ell(w)=%d" % length(w), font_size=28).set_color(STAR_COLOR).move_to(c + 0.95 * DOWN))
    assert_in_frame(*panels, *ells)
    for k in range(6):
        if k % 3 < 2:
            assert_apart(VGroup(panels[k], ells[k]), VGroup(panels[k + 1], ells[k + 1]), 0.4)
        if k < 3:
            assert_apart(VGroup(panels[k], ells[k]), VGroup(panels[k + 3], ells[k + 3]), 0.1)

    scene.say("$S_3$", " 的六個胞腔：每個不動旗旁邊配它的矩陣", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(p, shift=0.15 * UP) for p in panels], lag_ratio=0.25), run_time=2.4)
    scene.wait(SLOW * 0.4)
    scene.play(LaggedStart(*[FadeIn(e) for e in ells], lag_ratio=0.2), run_time=1.4)
    scene.say("星號數 ", "$0,1,1,2,2,3$", "：胞腔的維數就是逆序數", wait=SLOW * 0.9)
    scene.say("最大的 ", "$321$", " 有 3 顆星：", "$\\dim Fl(3)=3$", wait=SLOW * 0.8)
    scene.clear_stage()

    mat = CellMatrixMob(flag_cell_pattern(BOOK), cs=0.5).move_to(np.array([-2.2, 0.3, 0]))
    wl = Tex(r"w=426135", font_size=38).next_to(mat, UP, buff=0.4)
    cnt = VGroup(*[Tex(str(c), font_size=30).set_color(STAR_COLOR)
                   .move_to(np.array([mat.get_right()[0] + 0.45, mat.cell(i, 0).get_y(), 0]))
                   for i, c in enumerate(lehmer_code(BOOK))])
    tot = Tex(r"\ell(w)=3+1+3+0+0+0=7", font_size=36).set_color(OP_COLOR).move_to(np.array([3.6, 0.3, 0]))
    assert_in_frame(mat, wl, cnt, tot)
    assert_apart(VGroup(mat, cnt), tot, 0.4)

    scene.say("書上的例子：", "$w=426135$", wait=SLOW * 0.2)
    scene.play(FadeIn(wl), FadeIn(mat), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.2 * LEFT) for c in cnt], lag_ratio=0.2), run_time=1.2)
    scene.say("每列的星號數：右邊比它小、還沒用掉的數有幾個", wait=SLOW * 0.6)
    scene.play(Write(tot), run_time=1.0)
    scene.play(Indicate(mat.stars(), color=STAR_COLOR), run_time=1.0)
    scene.say("共 7 顆星 ＝ ", "$\\ell(426135)=7$", wait=SLOW * 0.8)


# ---------------------------------------------------------------- 4. 數旗：q-階乘與 Fano 平面
def part_count(scene):
    qf = Tex(r"[3]_q!=(1)(1+q)(1+q+q^2)=1+2q+2q^2+q^3", font_size=38).move_to(np.array([0, 2.45, 0]))
    q2 = Tex(r"q=2:\quad1+4+8+8=21", font_size=34).set_color(POS_COLOR).move_to(np.array([-3.5, 1.45, 0]))
    t73 = Tex(r"7\times3=21", font_size=34).move_to(np.array([-3.5, 0.6, 0]))
    brute = mixed("暴力數 ", "$\\mathbb F_2^3$", " 的旗：", "$21$", font_size=26).move_to(np.array([-3.5, -0.2, 0]))
    s4 = Tex(r"S_4:\quad1,3,5,6,5,3,1", font_size=34).move_to(np.array([0, -1.3, 0]))
    s4sum = Tex(r"q=2:\quad1+6+20+48+80+96+64=315=1\cdot3\cdot7\cdot15", font_size=34).set_color(POS_COLOR)
    s4sum.move_to(np.array([0, -2.2, 0]))
    fit(s4sum, 12.6)
    fc, R = np.array([3.6, 0.55, 0]), 1.25
    V = {1: fc + R * UP, 2: fc + R * np.array([-np.sqrt(3) / 2, -0.5, 0]),
         3: fc + R * np.array([np.sqrt(3) / 2, -0.5, 0])}
    M = {(1, 2): (V[1] + V[2]) / 2, (2, 3): (V[2] + V[3]) / 2, (1, 3): (V[1] + V[3]) / 2}
    sides = [Line(V[1], V[2]), Line(V[2], V[3]), Line(V[1], V[3])]
    meds = [Line(V[1], M[(2, 3)]), Line(V[2], M[(1, 3)]), Line(V[3], M[(1, 2)])]
    circ = Circle(radius=R / 2).move_to(fc)
    flines = VGroup(*sides, *meds, circ).set_stroke(GREY_B, 2)
    fdots = VGroup(*[Dot(p, radius=0.08) for p in list(V.values()) + list(M.values()) + [fc]]).set_color(WHITE)
    hl = VGroup(sides[0].copy(), sides[2].copy(), meds[0].copy()).set_stroke(OP_COLOR, 4)
    hdot = Dot(V[1], radius=0.12).set_color(OP_COLOR)
    fano = VGroup(flines, fdots)
    assert_in_frame(qf, q2, t73, brute, s4, s4sum, fano)
    assert_apart(qf, fano, 0.1)
    assert_apart(VGroup(q2, t73, brute), fano, 0.4)
    assert_apart(fano, s4, 0.1)
    for u, v in ((qf, q2), (q2, t73), (t73, brute), (brute, s4), (s4, s4sum)):
        assert_apart(u, v, 0.1)

    scene.say("數旗：每個胞腔記 ", "$q^{\\ell(w)}$", "，加起來是 ", "$q$", "-階乘", wait=SLOW * 0.2)
    scene.play(Write(qf), run_time=1.4)
    scene.say("係數 ", "$1,2,2,1$", " ＝ 長度 0、1、2、3 的置換個數", wait=SLOW * 0.8)
    scene.play(FadeIn(q2, shift=0.2 * DOWN), run_time=0.8)
    scene.say("$q=2$", "：在 ", "$\\mathbb F_2$", " 上，每個胞腔有 ", "$2^{\\ell(w)}$", " 個點，共 21 個旗", wait=SLOW * 0.6)
    scene.play(ShowCreation(flines), FadeIn(fdots), run_time=1.4)
    scene.say("$\\mathbb F_2^3$", " 的「點」與「線」：Fano 平面，7 個點、7 條線", wait=SLOW * 0.6)
    scene.play(FadeIn(hdot, scale=0.5), ShowCreation(hl), run_time=1.0)
    scene.play(FadeIn(t73, shift=0.2 * DOWN), run_time=0.8)
    scene.say("每個點在 3 條線上：", "$7\\times3=21$", wait=SLOW * 0.7)
    scene.play(FadeIn(brute, shift=0.2 * DOWN), run_time=0.8)
    scene.say("電腦把 ", "$\\mathbb F_2^3$", " 的旗一個個列出來：也是 21", wait=SLOW * 0.7)
    scene.play(FadeIn(s4, shift=0.2 * UP), run_time=0.8)
    scene.say("$S_4$", "：各長度的置換有 ", "$1,3,5,6,5,3,1$", " 個（共 24 個）", wait=SLOW * 0.6)
    scene.play(Write(s4sum), run_time=1.4)
    scene.say("$q=2$", "：", "$315$", " 個旗，和 ", "$[4]_2!=1\\cdot3\\cdot7\\cdot15$", " 一致，暴力數也是 315", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 5. Schubert 類與對偶
def part_classes(scene):
    c1 = Tex(r"\sigma_w=[\Omega_w]=[X_{w_0w}]\in H^{2\ell(w)}(Fl(m))", font_size=40).move_to(np.array([0, 2.4, 0]))
    c2 = Tex(r"\dim X_w=\ell(w),\qquad\operatorname{codim}\Omega_w=\ell(w)", font_size=34).set_color(MUTED_COLOR)
    c2.move_to(np.array([0, 1.5, 0]))
    pairs = Tex(r"123\leftrightarrow321,\qquad213\leftrightarrow231,\qquad132\leftrightarrow312", font_size=36)
    pairs.set_color(TEAL_B).move_to(np.array([0, 0.55, 0]))
    dual = Tex(r"\langle\sigma_u,\sigma_{w_0v}\rangle=\delta_{uv}", font_size=48).set_color(POS_COLOR)
    dual.move_to(np.array([0, -0.6, 0]))
    dfr = SurroundingRectangle(dual, buff=0.18, color=POS_COLOR)
    close = mixed("$m!$", " 個不動點，", "$m!$", " 個胞腔，", "$m!$", " 個類", font_size=32, color=OP_COLOR)
    close.move_to(np.array([0, -2.1, 0]))
    for m in (c1, c2, pairs):
        fit(m, 12.6)
    assert_in_frame(c1, c2, pairs, dual, dfr, close)
    for u, v in ((c1, c2), (c2, pairs), (pairs, dfr), (dfr, close)):
        assert_apart(u, v, 0.1)

    scene.say("每個胞腔的閉包給一個上同調類", wait=SLOW * 0.2)
    scene.play(Write(c1), run_time=1.4)
    scene.say("$\\sigma_w$", " 用 ", "$\\Omega_w=X_{w_0w}$", " 定義：餘維數是 ", "$\\ell(w)$", wait=SLOW * 0.8)
    scene.play(FadeIn(c2), run_time=0.8)
    scene.say("$X_w$", " 是 ", "$X^\\circ_w$", " 的閉包，維數 ", "$\\ell(w)$", "；乘上 ", "$w_0$", " 就把維數換成餘維數",
              wait=SLOW * 0.9)
    scene.play(FadeIn(pairs, shift=0.2 * DOWN), run_time=0.9)
    scene.say("$w_0w$", " 把每個值 ", "$i$", " 換成 ", "$4-i$", "：長度互補，加起來是 3", wait=SLOW * 0.8)
    scene.play(Write(dual), ShowCreation(dfr), run_time=1.2)
    scene.say("式 (2)：", "$\\sigma_u$", " 和 ", "$\\sigma_{w_0v}$", " 互為對偶基底", wait=SLOW * 0.9)
    scene.play(FadeIn(close, shift=0.2 * UP), run_time=0.9)
    scene.say("$m!$", " 個點，", "$m!$", " 個胞腔，", "$m!$", " 個類", wait=SLOW * 1.2)


class SceneF50FlagCells(ChuScene):
    def construct(self):
        self.show_header("旗流形：m! 個不動點與星號")
        check_math()
        part_fixed(self)
        self.clear_stage()
        part_cell(self)
        self.clear_stage()
        part_six(self)
        self.clear_stage()
        part_count(self)
        self.clear_stage()
        part_classes(self)
        self.wait(1.0)
