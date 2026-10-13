"""
Scene F36 —— Frobenius 特徵標公式（Fulton §7.3 Corollary 2、Exercises 6–7；原大綱卡 F717）
執行（在 codes/ 內）：manimgl scenes/sceneF36_frobenius.py SceneF36Frobenius

λ=(2,1)、k=2：ℓ=(3,1)，收集槽 x1^3 x2；χ_μ = [x1^3 x2](x1−x2)p_μ。
三個類各算一次得 2、0、−1（與 F33 的矩陣跡對上）；再用 χ 與 z=6,2,3 組回 s21=(p1^3−p3)/3。
"""
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import load, rep_matrix21
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob, perm_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import p_lambda, poly_mul, poly_sum, schur_poly, z_lambda

FRO = load("frobenius21")
CHAR = load("character_S3")
MAT = load("matrices21")
REPS = [(1, 2, 3), (2, 1, 3), (2, 3, 1)]          # e、(12)、(123)：三個類的代表（一行記法）
DELTA = {(1, 0): 1, (0, 1): -1}                   # x1 − x2
MU_TEX = [r"(1^3)", r"(2,1)", r"(3)"]
P_TEX = [r"(x_1+x_2)^3", r"(x_1^2+x_2^2)(x_1+x_2)", r"x_1^3+x_2^3"]
P_SHORT = [r"p_1^3", r"p_2p_1", r"p_3"]
SLOW = 1.8                                        # 旁白停頓倍率


def frob_parts(mu):
    """收集槽 x1^3 x2 的兩個來源：x1·[x1^2 x2]p_μ 與 −x2·[x1^3]p_μ。"""
    p = p_lambda(tuple(mu), 2)
    return p.get((2, 1), 0), -p.get((3, 0), 0)


def trace(m):
    return m[0][0] + m[1][1]


def check_math():
    lam, k = FRO["lambda"], FRO["k"]
    assert [lam[i] + k - 1 - i for i in range(k)] == FRO["ell"] == [3, 1]
    chis = []
    for t in FRO["targets"]:
        a, b = frob_parts(t["mu"])
        full = poly_mul(DELTA, p_lambda(tuple(t["mu"]), 2)).get((3, 1), 0)
        assert a + b == full == t["chi"]
        chis.append(full)
    assert [frob_parts(t["mu"]) for t in FRO["targets"]] == [(3, -1), (1, -1), (0, -1)]
    assert [t["mu"] for t in FRO["targets"]] == CHAR["types"]
    assert chis == CHAR["specht"]["21"] == [2, 0, -1]
    mats = [[list(r) for r in rep_matrix21(p)] for p in REPS]
    assert mats[1] == MAT["rho12"] and mats[2] == MAT["rho123"] and mats[0] == [[1, 0], [0, 1]]
    assert [trace(m) for m in mats] == chis
    assert CHAR["sizes"] == [1, 3, 2]
    assert CHAR["z"] == [z_lambda(tuple(m)) for m in CHAR["types"]] == [6, 2, 3]
    assert [Fraction(c, z) for c, z in zip(chis, CHAR["z"])] == [Fraction(1, 3), 0, Fraction(-1, 3)]
    lhs = {e: 3 * c for e, c in schur_poly((2, 1), 3).items()}
    rhs = poly_sum([p_lambda((1, 1, 1), 3), {e: -c for e, c in p_lambda((3,), 3).items()}])
    assert lhs == rhs                                   # 3 s21 = p1^3 − p3
    assert load("symmetric_functions")["frobenius_s21"] == "(p1^3-p3)/3"
    xi = CHAR["permutation"]["21"]
    assert xi == [3, 1, 0] and [x - 1 for x in xi] == chis


def coef_str(c):
    return "0" if c == 0 else f"{c:+d}"


def coef_color(c):
    return POS_COLOR if c > 0 else (NEG_COLOR if c < 0 else MUTED_COLOR)


def contrib_cell(term_tex, c):
    """「p_μ 裡被抽出的項 ⇒ 落進收集槽的係數」。"""
    return VGroup(
        Tex(term_tex, font_size=30, fill_color=GREY_A),
        Tex(r"\Rightarrow", font_size=26, fill_color=GREY_B),
        Tex(coef_str(c), font_size=38, fill_color=coef_color(c)),
    ).arrange(RIGHT, buff=0.15)


# ---------------------------------------------------------------- 1. 公式與收集槽
def part_formula(scene):
    scene.say("不算任何矩陣，能不能直接讀出特徵標？", wait=SLOW * 1.2)
    f1 = Tex(r"\chi^\lambda_\mu=[x_1^{\ell_1}\cdots x_k^{\ell_k}]\ \Delta\cdot p_\mu", font_size=46)
    f2 = Tex(r"\Delta=\prod_{i<j}(x_i-x_j),\qquad \ell_i=\lambda_i+k-i", font_size=36)
    VGroup(f1, f2).arrange(DOWN, buff=0.3).move_to(2.15 * UP)
    assert_in_frame(f1, f2)
    scene.play(Write(f1), run_time=1.5)
    scene.play(FadeIn(f2, shift=0.2 * DOWN), run_time=0.8)
    scene.say("Frobenius：特徵標就是一個係數；", "$\\Delta$", " 是 Vandermonde 乘積", wait=SLOW * 2.5)

    cs = 0.6
    d = YoungDiagramMob((2, 1), cell_size=cs, top_left=np.array([-5.6, -0.3, 0.0]))
    lam_lbl = Tex(r"\lambda=(2,1),\ k=2", font_size=34).next_to(d, UP, buff=0.3).align_to(d, LEFT)
    extra = Square(side_length=cs, stroke_color=OP_COLOR, fill_color=OP_COLOR, fill_opacity=0.35)
    extra.move_to(d.cell_center(0, 1) + cs * RIGHT)
    plus1 = Tex("+1", font_size=30, fill_color=OP_COLOR).next_to(extra, RIGHT, buff=0.15)
    plus0 = Tex("+0", font_size=30, fill_color=OP_COLOR).move_to(plus1).set_y(d.cell_center(1, 0)[1])
    stair = Tex(r"k-i", font_size=28, fill_color=OP_COLOR).next_to(VGroup(plus1, plus0), RIGHT, buff=0.2)
    left = VGroup(d, lam_lbl, extra, plus1, plus0, stair)

    ell = Tex(r"\ell=(2+1,\ 1+0)=(3,1)", font_size=36).move_to(np.array([0.4, -0.45, 0]))
    dlt = Tex(r"\Delta=x_1-x_2", font_size=36).move_to(np.array([0.4, -1.45, 0])).align_to(ell, LEFT)
    slot = Tex(r"[x_1^3x_2]", font_size=48, fill_color=OP_COLOR).move_to(np.array([4.7, -1.0, 0]))
    slot_box = SurroundingRectangle(slot, buff=0.25, color=OP_COLOR)
    slot_lbl = zh("收集槽", font_size=28, color=OP_COLOR).next_to(slot_box, UP, buff=0.15)
    assert_in_frame(left, ell, dlt, slot_box, slot_lbl)
    assert_apart(left, ell)
    assert_apart(ell, slot_box)
    assert_apart(f2, lam_lbl)

    scene.play(FadeIn(d), FadeIn(lam_lbl), run_time=0.8)
    scene.say("主例 ", "$\\lambda=(2,1)$", "，取 ", "$k=2$", " 個變數", wait=SLOW * 1.0)
    scene.play(GrowFromCenter(extra), FadeIn(plus1), FadeIn(plus0), FadeIn(stair), run_time=1.0)
    scene.say("每一列加上階梯 ", "$k-i$", "：第一列加 1、第二列加 0", wait=SLOW * 1.5)
    scene.play(Write(ell), run_time=1.0)
    scene.say("要讀的指數是 ", "$\\ell=(3,1)$", "，不是 ", "$\\lambda$", " 本身", wait=SLOW * 1.5)
    scene.play(Write(dlt), run_time=0.8)
    scene.play(FadeIn(slot), ShowCreation(slot_box), FadeIn(slot_lbl), run_time=1.0)
    scene.say("把 ", "$x_1^3x_2$", " 當成固定的收集槽：只追蹤落進來的項", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 2. 三個類各算一次
def part_classes(scene):
    top = Tex(r"\chi^{(2,1)}_\mu=[x_1^3x_2]\ (x_1-x_2)\cdot p_\mu", font_size=40).move_to(2.65 * UP)
    xs = [-5.85, -3.0, 0.45, 3.35, 5.9]
    heads = VGroup(Tex(r"\mu", font_size=36), Tex(r"p_\mu", font_size=36),
                   Tex(r"x_1\times x_1^2x_2", font_size=32), Tex(r"-x_2\times x_1^3", font_size=32),
                   Tex(r"\chi", font_size=38))
    for h, x in zip(heads, xs):
        h.set_fill(GREY_A).move_to(np.array([x, 1.55, 0]))
    rule = Line(np.array([-6.5, 1.1, 0]), np.array([6.5, 1.1, 0]), stroke_color=GREY_D, stroke_width=2)
    ys = [0.45, -0.75, -1.95]
    rows = []
    for r, t in enumerate(FRO["targets"]):
        a, b = frob_parts(t["mu"])
        term_a = {3: r"3x_1^2x_2", 1: r"x_1^2x_2", 0: r"\text{---}"}[a]
        cells = [Tex(MU_TEX[r], font_size=36), Tex(P_TEX[r], font_size=32),
                 contrib_cell(term_a, a), contrib_cell(r"x_1^3", b),
                 Tex(str(t["chi"]), font_size=44, fill_color=OP_COLOR)]
        for c, x in zip(cells, xs):
            c.move_to(np.array([x, ys[r], 0]))
        box = SurroundingRectangle(cells[4], buff=0.15, color=OP_COLOR)
        for c1, c2 in zip(cells, cells[1:]):
            assert_apart(c1, c2, 0.15)
        assert_in_frame(*cells, box)
        rows.append((cells, box))
    for h1, h2 in zip(heads, heads[1:]):
        assert_apart(h1, h2, 0.15)
    assert_in_frame(top, heads)

    scene.play(FadeIn(top), FadeIn(heads), ShowCreation(rule), run_time=1.0)
    scene.say("兩個來源：", "$x_1$", " 乘上 ", "$x_1^2x_2$", "，或 ", "$-x_2$", " 乘上 ", "$x_1^3$", wait=SLOW * 2.0)
    captions = [
        ("恆等：", "$x_1\\cdot 3x_1^2x_2$", " 給 ", "$+3$", "，", "$-x_2\\cdot x_1^3$", " 給 ", "$-1$", "，合起來 2"),
        ("對換：只剩兩個相反的貢獻 ", "$+1$", " 與 ", "$-1$", "，相消成 0"),
        ("3-循環：", "$p_3$", " 沒有 ", "$x_1^2x_2$", " 項，只剩 ", "$-x_2\\cdot x_1^3$", "，得 ", "$-1$"),
    ]
    for (cells, box), cap in zip(rows, captions):
        scene.play(FadeIn(cells[0]), Write(cells[1]), run_time=1.0)
        scene.play(TransformFromCopy(cells[1], cells[2]), run_time=1.0)
        scene.play(TransformFromCopy(cells[1], cells[3]), run_time=1.0)
        scene.say(*cap, wait=SLOW * 1.0)
        scene.play(TransformFromCopy(VGroup(cells[2][2], cells[3][2]), cells[4]), ShowCreation(box), run_time=1.0)
        scene.wait(SLOW * 1.5)
    scene.say("其他單項式都落不進收集槽，完全不必展開", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 3. 和矩陣的跡核對
def part_traces(scene):
    xs = [-2.6, 0.9, 4.4]
    lbl_x = -5.3
    row_y = [2.3, 1.0, -0.4, -1.6]
    labels = VGroup(zh("類代表", font_size=26, color=GREY_A), Tex(r"\rho(\sigma)", font_size=34),
                    Tex(r"\operatorname{tr}\rho(\sigma)", font_size=34), zh("收集槽係數", font_size=26, color=GREY_A))
    for m, y in zip(labels, row_y):
        m.move_to(np.array([lbl_x, y, 0]))
    cols = []
    for j, p in enumerate(REPS):
        mat = [list(r) for r in rep_matrix21(p)]
        a, b = mat[0][0], mat[1][1]
        name = VGroup(Tex(perm_tex(p), font_size=36),
                      zh(f"（{CHAR['sizes'][j]} 個）", font_size=22, color=MUTED_COLOR)).arrange(RIGHT, buff=0.1)
        mm = MatrixMob(mat, font_size=34, h_buff=0.7, v_buff=0.5, colors={(0, 0): OP_COLOR, (1, 1): OP_COLOR})
        bs = f"({b})" if b < 0 else str(b)
        tr = Tex(f"{a}+{bs}={a + b}", font_size=34)
        fr = Tex(str(CHAR["specht"]["21"][j]), font_size=40, fill_color=OP_COLOR)
        ok = Tex(r"\checkmark", font_size=34, fill_color=POS_COLOR).next_to(fr, RIGHT, buff=0.25)
        col = [name, mm, tr, fr]
        for m, y in zip(col, row_y):
            m.move_to(np.array([xs[j], y, 0]))
        ok.next_to(fr, RIGHT, buff=0.25)
        cols.append(col + [ok])
    for j in range(2):
        for r in range(4):
            assert_apart(cols[j][r], cols[j + 1][r], 0.2)
    assert_in_frame(labels, *[m for c in cols for m in c])
    assert_apart(labels, VGroup(*[c[r] for c in cols for r in range(4)]))

    scene.say("和 F33 對一下：同樣三個類，逐類取矩陣的跡", wait=SLOW * 0.5)
    scene.play(FadeIn(labels[:3]), *[FadeIn(VGroup(c[0], c[1])) for c in cols], run_time=1.2)
    scene.wait(SLOW * 1.0)
    scene.play(*[TransformFromCopy(VGroup(c[1].entry(0, 0), c[1].entry(1, 1)), c[2]) for c in cols], run_time=1.2)
    scene.wait(SLOW * 1.5)
    scene.play(FadeIn(labels[3]), *[FadeIn(c[3], shift=0.2 * UP) for c in cols], run_time=0.8)
    scene.play(*[Write(c[4]) for c in cols], run_time=0.8)
    scene.say("跡是 ", "$2,\\ 0,\\ -1$", "；收集槽的係數也是 ", "$2,\\ 0,\\ -1$", wait=SLOW * 2.5)
    scene.say("一個係數就等於一整個矩陣的跡：這就是 Frobenius 公式的威力", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 4. 組回 s21
def part_assemble(scene):
    f = Tex(r"s_\lambda=\sum_\mu\frac{\chi^\lambda_\mu}{z_\mu}\,p_\mu", font_size=42).move_to(2.45 * UP)
    xs = [-0.6, 1.9, 4.4]
    lbl_x = -3.6
    ys = [1.25, 0.5, -0.25, -1.0]
    lbls = VGroup(Tex(r"\mu", font_size=32), Tex(r"\chi^{(2,1)}_\mu", font_size=32),
                  Tex(r"z_\mu", font_size=32), Tex(r"p_\mu", font_size=32))
    for m, y in zip(lbls, ys):
        m.set_fill(GREY_A).move_to(np.array([lbl_x, y, 0]))
    table = []
    for j in range(3):
        chi, z = CHAR["specht"]["21"][j], CHAR["z"][j]
        col = [Tex(MU_TEX[j], font_size=32, fill_color=GREY_A),
               Tex(str(chi), font_size=34, fill_color=OP_COLOR),
               Tex(str(z), font_size=34, fill_color=ROW_COLOR),
               Tex(P_SHORT[j], font_size=34)]
        for m, y in zip(col, ys):
            m.move_to(np.array([xs[j], y, 0]))
        table.append(col)
    terms = [Tex(r"s_{21}=", font_size=40)]
    for j in range(3):
        chi, z = CHAR["specht"]["21"][j], CHAR["z"][j]
        sgn = "" if j == 0 else "+"
        terms.append(Tex(sgn + r"\frac{" + str(chi) + "}{" + str(z) + "}" + P_SHORT[j], font_size=40))
    eq = Tex("=", font_size=44)
    final = Tex(r"\frac{p_1^3-p_3}{3}", font_size=44, fill_color=POS_COLOR)
    line = VGroup(*terms, eq, final).arrange(RIGHT, buff=0.22).move_to(2.15 * DOWN)
    box = SurroundingRectangle(final, buff=0.12, color=POS_COLOR)
    assert_in_frame(f, lbls, line, box, *[m for c in table for m in c])
    assert_apart(VGroup(*[c[3] for c in table]), line)
    assert_apart(f, VGroup(*[c[0] for c in table]))

    scene.say("反過來：用 ", "$\\chi$", " 和 ", "$z_\\mu$", " 把 Schur 函數組回 power sum", wait=SLOW * 0.5)
    scene.play(Write(f), run_time=1.2)
    scene.play(FadeIn(lbls), *[FadeIn(VGroup(*c)) for c in table], run_time=1.0)
    scene.say("$z_\\mu=6,2,3$", "：類的大小是 ", "$6/z_\\mu=1,3,2$", wait=SLOW * 2.0)
    scene.play(FadeIn(terms[0]), run_time=0.5)
    for j in range(3):
        scene.play(TransformFromCopy(VGroup(table[j][1], table[j][2], table[j][3]), terms[j + 1]), run_time=1.0)
    scene.say("中間那項係數是 0，直接消失", wait=SLOW * 1.0)
    scene.play(FadeIn(eq), Write(final), ShowCreation(box), run_time=1.2)
    scene.say("$s_{21}=(p_1^3-p_3)/3$", "：和對稱函數那一段的展開一致", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 5. 負號的意義
def part_sign(scene):
    scene.say("為什麼係數可以是負的？", wait=SLOW * 1.0)
    r1 = VGroup(Tex(r"\xi^{(2,1)}=", font_size=36), Tex(r"3,\ 1,\ 0", font_size=36, fill_color=ROW_COLOR))
    r2 = VGroup(Tex(r"\chi^{(2,1)}=\xi-1=", font_size=36), Tex(r"2,\ 0,\ -1", font_size=36, fill_color=OP_COLOR))
    for r in (r1, r2):
        r.arrange(RIGHT, buff=0.15)
    VGroup(r1, r2).arrange(DOWN, buff=0.55, aligned_edge=RIGHT).move_to(np.array([-3.2, 1.6, 0]))
    d1 = zh("固定的 tabloid 個數：一定 ≥ 0", font_size=26, color=ROW_COLOR).next_to(r1, RIGHT, buff=0.5)
    d2 = zh("跡＝特徵值之和：可以是負的", font_size=26, color=OP_COLOR).next_to(r2, RIGHT, buff=0.5)
    d2.align_to(d1, LEFT)
    rot = Tex(r"\rho(1\,2\,3)\sim\text{rot}_{120^\circ}", font_size=34).move_to(np.array([-3.0, -0.5, 0]))
    eig = Tex(r"e^{2\pi i/3}+e^{-2\pi i/3}=2\cos 120^\circ=-1", font_size=34).next_to(rot, DOWN, buff=0.4)
    eig.align_to(rot, LEFT)
    R, c0 = 0.9, np.array([4.6, -1.0, 0])
    circ = Circle(radius=R, stroke_color=GREY_C, stroke_width=2).move_to(c0)
    axis = Line(c0 + 1.25 * R * LEFT, c0 + 1.25 * R * RIGHT, stroke_color=GREY_D, stroke_width=1.5)
    pts = [c0 + R * np.array([np.cos(a), np.sin(a), 0]) for a in (2 * PI / 3, -2 * PI / 3)]
    dots = VGroup(*[Dot(p, radius=0.07, fill_color=OP_COLOR) for p in pts])
    tip = Dot(c0 + R * LEFT, radius=0.08, fill_color=NEG_COLOR)
    tip_lbl = Tex("-1", font_size=30, fill_color=NEG_COLOR).next_to(tip, LEFT, buff=0.12)
    arrows = VGroup(Arrow(c0, pts[0], buff=0, stroke_color=OP_COLOR, stroke_width=3),
                    Arrow(c0, pts[1], buff=0, stroke_color=OP_COLOR, stroke_width=3))
    wheel = VGroup(circ, axis, arrows, dots, tip, tip_lbl)
    assert_in_frame(r1, r2, d1, d2, rot, eig, wheel)
    assert_apart(VGroup(rot, eig), wheel)
    assert_apart(r2, rot)

    scene.play(FadeIn(r1), FadeIn(d1), run_time=0.8)
    scene.say("置換模組 ", "$M^{(2,1)}$", " 的特徵標數固定的 tabloid：", "$3,1,0$", wait=SLOW * 1.5)
    scene.play(FadeIn(r2), FadeIn(d2), run_time=0.8)
    scene.say("扣掉平凡表示才是 ", "$\\chi^{(2,1)}$", "：它是跡，不是在數東西", wait=SLOW * 1.5)
    scene.play(Write(rot), FadeIn(VGroup(circ, axis)), run_time=1.0)
    scene.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(dots), run_time=1.0)
    scene.play(Write(eig), FadeIn(tip), FadeIn(tip_lbl), run_time=1.2)
    scene.say("120° 旋轉的兩個特徵值加起來是 ", "$-1$", "：負號來自跡", wait=SLOW * 2.0)
    scene.say("在公式裡，負號來自 ", "$\\Delta$", " 的 ", "$-x_2$", "；不是「負一個固定的表」", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 6. 收束
def part_summary(scene):
    lines = VGroup(
        mixed(r"$\Delta=\prod_{i<j}(x_i-x_j)$", "：Vandermonde 帶來符號", font_size=30),
        mixed("目標指數是 ", r"$\ell_i=\lambda_i+k-i$", "，不是 ", r"$\lambda$", font_size=30),
        mixed("$(2,1)$", " 的三個類讀出 ", r"$2,\ 0,\ -1$", "，正是矩陣的跡", font_size=30),
    ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(0.3 * UP)
    marks = VGroup(*[Dot(radius=0.07, fill_color=OP_COLOR).next_to(l, LEFT, buff=0.3) for l in lines])
    assert_in_frame(lines, marks)
    scene.say("收束：讀一個係數，就讀出一個跡", wait=SLOW * 0.5)
    for l, m in zip(lines, marks):
        scene.play(FadeIn(m), FadeIn(l, shift=0.2 * RIGHT), run_time=0.9)
        scene.wait(SLOW * 1.5)
    scene.say("下一步：同一張表，換到 ", "$S_{n-1}$", " 和 ", "$S_{n+1}$", " 去看", wait=SLOW * 1.5)


class SceneF36Frobenius(ChuScene):
    def construct(self):
        self.show_header("Frobenius 特徵標公式")
        check_math()
        part_formula(self)
        self.clear_stage()
        part_classes(self)
        self.clear_stage()
        part_traces(self)
        self.clear_stage()
        part_assemble(self)
        self.clear_stage()
        part_sign(self)
        self.clear_stage()
        part_summary(self)
        self.wait(1.0)
