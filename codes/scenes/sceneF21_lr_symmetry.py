"""
Scene F21 —— LR 數的對稱性、c = 0 的判別、推論 3 與 4（Fulton《Young Tableaux》§5.1，書 p.62–63）

    同一個數字的三張臉：c^{(4,2,1)}_{(2,1),(3,1)} = c^{(4,2,1)}_{(3,1),(2,1)} = c^{(3,2,1,1)}_{(2,1),(2,1,1)} = 2（推論 2）
    卡住的拼圖：λ=(2,2)、μ=(3,2)、ν=(3,3,3)：格數對、λ,μ ⊂ ν，但 λ*μ = (5,4,2,2)/(2,2) 第 3 列只有 2 格，
        ν 穿出外框 → c = 0（推論 2(v)）；μ*λ = (5,5,3,2)/(3,3) 塞得進去，但數字一樣是 0
    推論 3：S_(2,1)·S_(2,1) = S(4,2)+S(4,1,1)+S(3,3)+2S(3,2,1)+S(3,1,1,1)+S(2,2,2)+S(2,2,1,1)
    推論 4：S_(3,2,1)/(2,1) = S(3) + 2S(2,1) + S(1,1,1)
    多項式（m = 3）：s(2,1)² 乘開 19 種單項式 = s(4,2)+s(4,1,1)+s(3,3)+2s(3,2,1)+s(2,2,2)；
        代 1：8×8 = 64 = 27+10+10+2·8+1

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF21_lr_symmetry.py SceneF21LRSymmetry
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed
from utils.tableaux import (
    CH5_S21_SQUARED,
    CH5_ZERO,
    conjugate,
    contains,
    hook_content_count,
    lattice_tableau,
    lr_coefficient,
    lr_product,
    poly_mul,
    poly_sum,
    schur_expand,
    schur_poly,
    skew_decomposition,
    skew_shape,
    ssyt,
    star,
    young_boxes,
)

FACE = ((2, 1), (3, 1), (4, 2, 1))           # (λ, μ, ν)
FACE_C = 2
STAR_LM = ((5, 4, 2, 2), (2, 2))             # λ*μ 的 (外框, 空白)
STAR_ML = ((5, 5, 3, 2), (3, 3))             # μ*λ
SQ_LAM = (2, 1)
SKEW_EX = ((3, 2, 1), (2, 1))
SKEW_DEC = {(3,): 1, (2, 1): 2, (1, 1, 1): 1}
M = 3
N_MONO = 19
S21_AT_1 = 8

L_COLOR, M_COLOR, N_COLOR = BLUE_C, GREEN_C, GOLD


def check_math():
    lam, mu, nu = FACE
    assert lr_coefficient(lam, mu, nu) == lr_coefficient(mu, lam, nu) == FACE_C
    assert lr_coefficient(conjugate(lam), conjugate(mu), conjugate(nu)) == FACE_C
    lam, mu, nu = CH5_ZERO
    assert sum(nu) == sum(lam) + sum(mu) and contains(nu, lam) and contains(nu, mu)
    assert lr_coefficient(lam, mu, nu) == lr_coefficient(mu, lam, nu) == 0
    assert skew_shape(star(lattice_tableau(lam), lattice_tableau(mu))) == STAR_LM
    assert skew_shape(star(lattice_tableau(mu), lattice_tableau(lam))) == STAR_ML
    assert not contains(STAR_LM[0], nu) and contains(STAR_ML[0], nu)
    assert lr_product(SQ_LAM, SQ_LAM) == CH5_S21_SQUARED
    assert skew_decomposition(*SKEW_EX) == SKEW_DEC
    assert all(lr_coefficient(SKEW_EX[1], m, SKEW_EX[0]) == c for m, c in SKEW_DEC.items())
    s = schur_poly(SQ_LAM, M)
    sq = poly_mul(s, s)
    assert len(sq) == N_MONO and sum(s.values()) == S21_AT_1 == len(ssyt(SQ_LAM, M))
    assert schur_expand(sq, M) == {nu: c for nu, c in CH5_S21_SQUARED.items() if len(nu) <= M}
    assert sq == poly_sum({e: c * v for e, v in schur_poly(nu, M).items()} for nu, c in CH5_S21_SQUARED.items())
    assert sum(sq.values()) == S21_AT_1 ** 2 == sum(c * hook_content_count(nu, M) for nu, c in CH5_S21_SQUARED.items())


def diagram(lam, cs, color, top_left=None, center=ORIGIN, opacity=0.4):
    kw = {"top_left": np.array(top_left, dtype=float)} if top_left is not None else {"center": center}
    return YoungDiagramMob(lam, cell_size=cs, fill_color=color, fill_opacity=opacity, **kw)


def c_tex(lam, mu, nu, value=None):
    s = f"c^{{{tuple_str(nu)}}}_{{{tuple_str(lam)},{tuple_str(mu)}}}"
    return s if value is None else s + f"={value}"


# =============================================================================
# 第 1 段：同一個數字的三張臉
# =============================================================================
def face_card(lam, mu, nu, x, lam_color, mu_color, cs=0.3):
    """VGroup(公式, ν 圖, 左下圖, 右下圖)；公式是 c^ν_{λμ}=值。"""
    f = Tex(c_tex(lam, mu, nu, lr_coefficient(lam, mu, nu)), font_size=32).move_to([x, 2.45, 0])
    dn = diagram(nu, cs, N_COLOR, top_left=(x - nu[0] * cs / 2, 1.75, 0))
    low = VGroup(diagram(lam, cs, lam_color), diagram(mu, cs, mu_color)).arrange(RIGHT, buff=0.4, aligned_edge=UP)
    low.move_to([x, -0.15, 0], aligned_edge=UP)
    return VGroup(f, dn, low[0], low[1])


def transposed_target(d, card_dn_tl, cs):
    """d 的複本，每一格 (i,j) 搬到 (j,i)：轉置的動畫目標。"""
    t = d.copy()
    for src, dst in zip(d.cells, t.cells):
        i, j = src.ij
        dst.move_to(card_dn_tl + (i + 0.5) * cs * RIGHT + (j + 0.5) * cs * DOWN)
    return t


def part_faces(scene):
    lam, mu, nu = FACE
    cs = 0.3
    c1 = face_card(lam, mu, nu, 0.0, L_COLOR, M_COLOR)
    c2 = face_card(mu, lam, nu, -4.6, M_COLOR, L_COLOR)
    c3 = face_card(conjugate(lam), conjugate(mu), conjugate(nu), 4.6, L_COLOR, M_COLOR)
    a_left = Arrow([-1.25, 1.0, 0], [-3.4, 1.0, 0], buff=0, stroke_width=4, fill_color=GREY_B)
    a_right = Arrow([1.25, 1.0, 0], [3.4, 1.0, 0], buff=0, stroke_width=4, fill_color=GREY_B)
    l_left = mixed("交換 ", "$\\lambda,\\mu$", font_size=22, color=MUTED_COLOR).next_to(a_left, UP, buff=0.1)
    l_right = mixed("全部轉置", font_size=22, color=MUTED_COLOR).next_to(a_right, UP, buff=0.1)
    names = VGroup(*[Tex(n, font_size=28, fill_color=col).next_to(c1[k], LEFT, buff=0.2)
                     for k, n, col in ((1, r"\nu", N_COLOR), (2, r"\lambda", L_COLOR))],
                   Tex(r"\mu", font_size=28, fill_color=M_COLOR).next_to(c1[3], RIGHT, buff=0.2))
    law = Tex(r"c^{\nu}_{\lambda\mu}=c^{\nu}_{\mu\lambda}=c^{\tilde\nu}_{\tilde\lambda\tilde\mu}", font_size=44)
    law.move_to([0, -1.85, 0])
    lfr = SurroundingRectangle(law, buff=0.15, color=YELLOW, stroke_width=3)
    assert_in_frame(c1, c2, c3, l_left, l_right, names, lfr)
    for a, b in ((c2, c1), (c1, c3)):
        assert_apart(a[1:], b[1:], gap=0.8)
        assert_apart(a[0], b[0], gap=0.3)
    for a, lab in ((a_left, l_left), (a_right, l_right)):
        for card in (c1, c2, c3, *names):
            assert_apart(VGroup(a, lab), card, gap=0.08)
    assert_apart(VGroup(c1, c2, c3, names), lfr, gap=0.15)

    scene.say("同一個數字的三張臉：先看 ", "$" + c_tex(lam, mu, nu) + f"={FACE_C}$")
    scene.play(FadeIn(c1[0]), FadeIn(c1[1:], shift=0.1 * UP), FadeIn(names), run_time=0.9)
    scene.wait(1.5)
    scene.say("第二張臉：把 ", "$\\lambda$", " 和 ", "$\\mu$", " 對調，數字不變")
    scene.play(GrowArrow(a_left), FadeIn(l_left), run_time=0.5)
    scene.play(TransformFromCopy(c1[1], c2[1]), TransformFromCopy(c1[2], c2[3], path_arc=-PI / 3),
               TransformFromCopy(c1[3], c2[2], path_arc=PI / 3), run_time=1.1)
    scene.play(FadeIn(c2[0], shift=0.1 * DOWN), run_time=0.5)
    scene.wait(1.4)
    scene.say("第三張臉：三個圖一起沿對角線翻過去（轉置），數字還是 ", f"${FACE_C}$")
    scene.play(GrowArrow(a_right), FadeIn(l_right), run_time=0.5)
    flips = []
    for k in (1, 2, 3):
        tl = c3[k].cells[0].get_corner(UL)
        flips.append(Transform(c1[k].copy(), transposed_target(c1[k], tl, cs), path_arc=PI / 2))
    scene.play(*flips, run_time=1.3)
    scene.play(FadeIn(c3[0], shift=0.1 * DOWN), run_time=0.5)
    scene.wait(1.4)
    scene.say("推論 2：換個角度數同一批表，三張臉永遠相等")
    scene.play(FadeIn(law), ShowCreation(lfr), run_time=0.9)
    scene.wait(2.4)


# =============================================================================
# 第 2 段：卡住的拼圖——ν 穿出 λ*μ，c = 0
# =============================================================================
def star_diagram(outer_inner, n_low_rows, cs, top_left, low_color, high_color):
    """λ*μ 這類斜形：空白的長方形塗灰，右上（前 n_high 列）與左下各塗一色。"""
    outer, inner = outer_inner
    d = YoungDiagramMob(outer, cell_size=cs, top_left=np.array(top_left, dtype=float))
    inner = tuple(inner) + (0,) * (len(outer) - len(inner))
    n_high = len(outer) - n_low_rows
    for i, j in young_boxes(outer):
        if j < inner[i]:
            d.cell(i, j).set_fill(GREY_D, opacity=0.6)
        else:
            d.cell(i, j).set_fill(high_color if i < n_high else low_color, opacity=0.45)
    return d


def nu_overlay(nu, outer, cs, top_left, ok_color):
    tl = np.array(top_left, dtype=float)
    d = YoungDiagramMob(nu, cell_size=cs, top_left=tl, stroke_color=YELLOW, stroke_width=6)
    out = [(i, j) for i, j in young_boxes(nu) if (i, j) not in set(young_boxes(outer))]
    for b in out:
        d.cell(*b).set_fill(RED, opacity=0.75)
    for b in young_boxes(nu):
        if b not in out:
            d.cell(*b).set_stroke(ok_color if not out else YELLOW)
    return d, out


def part_stuck(scene):
    lam, mu, nu = CH5_ZERO
    cs = 0.5
    head = mixed("$\\lambda=" + tuple_str(lam) + "$", "、", "$\\mu=" + tuple_str(mu) + "$", "、",
                 "$\\nu=" + tuple_str(nu) + "$", font_size=26).move_to([-6.3, 2.6, 0], aligned_edge=LEFT)
    tl1, tl2 = (-6.3, 1.9, 0), (-2.75, 1.9, 0)
    d1 = star_diagram(STAR_LM, len(lam), cs, tl1, L_COLOR, M_COLOR)
    d2 = star_diagram(STAR_ML, len(mu), cs, tl2, M_COLOR, L_COLOR)
    n1, out1 = nu_overlay(nu, STAR_LM[0], cs, tl1, OK_COLOR)
    n2, out2 = nu_overlay(nu, STAR_ML[0], cs, tl2, OK_COLOR)
    assert out1 == [(2, 2)] and out2 == []
    lab1 = Tex(r"\lambda*\mu", font_size=32).next_to(d1, DOWN, buff=0.2)
    lab2 = Tex(r"\mu*\lambda", font_size=32).next_to(d2, DOWN, buff=0.2)
    lab2.match_y(lab1)
    r1 = mixed("$|\\nu|=" + f"{sum(nu)}={sum(lam)}+{sum(mu)}" + "$", font_size=26)
    r2 = mixed("$\\lambda\\subset\\nu$", "，", "$\\mu\\subset\\nu$", font_size=26)
    checks = VGroup(*[VGroup(r, Tex(r"\checkmark", font_size=34, fill_color=OK_COLOR)).arrange(RIGHT, buff=0.25)
                      for r in (r1, r2)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    checks.move_to([1.2, 1.35, 0], aligned_edge=LEFT)
    res = Tex(c_tex(lam, mu, nu, lr_coefficient(lam, mu, nu)), font_size=44, fill_color=YELLOW)
    res.move_to([3.5, -0.2, 0])
    rfr = SurroundingRectangle(res, buff=0.15, color=YELLOW, stroke_width=3)
    e1 = mixed("滑動時格子只往左上搬：外框只縮不長", font_size=24)
    e2 = mixed("推論 2：", "$c^{\\nu}_{\\lambda\\mu}$", "＝", "$\\lambda*\\mu$", " 上會滑成 ", "$\\nu$",
               " 形某個表的斜表個數", font_size=24)
    expl = VGroup(e1, e2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-6.3, -1.75, 0], aligned_edge=LEFT)
    stick = mixed("穿出去了！", font_size=24, color=RED).next_to(n1.cell(*out1[0]), RIGHT, buff=0.15)
    stick.shift(0.35 * DOWN)
    assert_in_frame(head, d1, d2, n1, n2, lab1, lab2, checks, rfr, expl, stick)
    assert_apart(head, VGroup(d1, d2, checks), gap=0.15)
    assert_apart(VGroup(d1, lab1, stick), VGroup(d2, lab2), gap=0.2)
    assert_apart(VGroup(d2, lab2), VGroup(checks, rfr), gap=0.3)
    assert_apart(checks, rfr, gap=0.2)
    assert_apart(VGroup(d1, d2, lab1, lab2, rfr, stick), expl, gap=0.15)

    scene.say("「卡住的拼圖」：", "$\\lambda=" + tuple_str(lam) + "$", "、", "$\\mu=" + tuple_str(mu) + "$",
              "、", "$\\nu=" + tuple_str(nu) + "$")
    scene.play(FadeIn(head), run_time=0.6)
    scene.wait(0.6)
    scene.say("表面條件都過關：格數對得上，", "$\\lambda,\\mu$", " 也都放得進 ", "$\\nu$")
    scene.play(LaggedStart(*[FadeIn(c, shift=0.1 * LEFT) for c in checks], lag_ratio=0.4), run_time=1.0)
    scene.wait(1.0)
    scene.say("把 ", "$\\lambda$", " 放左下、", "$\\mu$", " 放右上，中間空一塊：斜形 ", "$\\lambda*\\mu$")
    scene.play(FadeIn(d1, shift=0.1 * UP), FadeIn(lab1), run_time=0.8)
    scene.wait(1.0)
    scene.say("推論 2：", "$c^{\\nu}_{\\lambda\\mu}$", " 也是 ", "$\\lambda*\\mu$", " 上會滑成 ", "$\\nu$",
              " 形表的斜表個數")
    scene.play(FadeIn(e2), run_time=0.6)
    scene.wait(1.4)
    scene.say("但滑動只會把格子往左上搬，外框只縮不長")
    scene.play(FadeIn(e1), run_time=0.6)
    scene.wait(1.2)
    scene.say("把 ", "$\\nu$", " 疊上去：第 3 列要 3 格，外框只有 2 格")
    scene.play(ShowCreation(n1), run_time=1.0)
    scene.play(Indicate(n1.cell(*out1[0]), color=RED, scale_factor=1.3), FadeIn(stick), run_time=0.8)
    scene.say("塞不進去，所以 ", "$" + c_tex(lam, mu, nu) + "=0$")
    scene.play(FadeIn(res, scale=1.2), ShowCreation(rfr), run_time=0.7)
    scene.wait(1.4)
    scene.say("換成 ", "$\\mu*\\lambda$", " 塞得進去、看不出來；但三張臉是同一個數，仍然是 0")
    scene.play(FadeIn(d2, shift=0.1 * UP), FadeIn(lab2), run_time=0.7)
    scene.play(ShowCreation(n2), run_time=0.8)
    scene.wait(2.4)


# =============================================================================
# 第 3 段：推論 3、4（表環裡的乘法表）
# =============================================================================
def sum_row(lhs, terms, letter, fs=30):
    """lhs = Σ c·letter_ν；回傳 (VGroup, [係數 > 1 的項])。"""
    parts, hl = [Tex(lhs + "=", font_size=fs)], []
    for k, (lam, c) in enumerate(terms):
        if k:
            parts.append(Tex("+", font_size=fs))
        t = Tex(f"{letter}_{{{tuple_str(lam)}}}", font_size=fs)
        if c > 1:
            t = VGroup(Tex(str(c), font_size=fs, fill_color=YELLOW), t).arrange(RIGHT, buff=0.05)
            hl.append(t)
        parts.append(t)
    return VGroup(*parts).arrange(RIGHT, buff=0.1), hl


def part_corollaries(scene):
    prod = sorted(lr_product(SQ_LAM, SQ_LAM).items(), reverse=True)
    dec = sorted(skew_decomposition(*SKEW_EX).items(), reverse=True)
    c3 = mixed("推論 3：", "$S_\\lambda\\cdot S_\\mu=\\sum_\\nu c^{\\nu}_{\\lambda\\mu}\\,S_\\nu$", font_size=28)
    n3 = mixed("$S_\\lambda$", "＝形狀 ", "$\\lambda$", " 的所有表相加；每個 ", "$\\nu$", " 形的表恰好被拆出 ",
               "$c^{\\nu}_{\\lambda\\mu}$", " 次", font_size=22, color=MUTED_COLOR)
    ex3, hl3 = sum_row(r"S_{(2,1)}\cdot S_{(2,1)}", prod, "S", fs=36)
    c4 = mixed("推論 4：", "$S_{\\nu/\\lambda}=\\sum_\\mu c^{\\nu}_{\\lambda\\mu}\\,S_\\mu$", font_size=28)
    n4 = mixed("$S_{\\nu/\\lambda}$", "＝", "$\\nu/\\lambda$", " 上所有斜表 rectify 後相加", font_size=22,
               color=MUTED_COLOR)
    ex4, hl4 = sum_row(r"S_{(3,2,1)/(2,1)}", dec, "S", fs=38)
    block = VGroup(c3, n3, ex3, c4, n4, ex4).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    block.move_to([-6.3, 0.15, 0], aligned_edge=LEFT)
    for m in (ex3, ex4):
        m.shift(0.4 * RIGHT)
    c4.shift(0.25 * DOWN)
    n4.shift(0.25 * DOWN)
    ex4.shift(0.25 * DOWN)
    assert_in_frame(c3, n3, ex3, c4, n4, ex4)
    for a, b in ((c3, n3), (n3, ex3), (ex3, c4), (c4, n4), (n4, ex4)):
        assert_apart(a, b, gap=0.12)

    scene.say("推論 3：在表環裡，", "$S_\\lambda$", " 的乘法表由 LR 數決定")
    scene.play(FadeIn(c3), FadeIn(n3), run_time=0.8)
    scene.wait(1.2)
    scene.play(FadeIn(ex3, shift=0.1 * UP), run_time=0.9)
    scene.say("係數 2：剛才的每個 ", "$(3,2,1)$", " 形的表，都恰好有 2 種拆法")
    scene.play(*[Indicate(t, color=YELLOW) for t in hl3], run_time=0.9)
    scene.wait(1.4)
    scene.say("推論 4：斜表滑完之後，形狀 ", "$\\mu$", " 的每個表恰好出現 ", "$c^{\\nu}_{\\lambda\\mu}$", " 次")
    scene.play(FadeIn(c4), FadeIn(n4), run_time=0.8)
    scene.play(FadeIn(ex4, shift=0.1 * UP), run_time=0.8)
    scene.wait(0.6)
    scene.play(*[Indicate(t, color=YELLOW) for t in hl4], run_time=0.8)
    scene.wait(2.2)


# =============================================================================
# 第 4 段：在 m = 3 個變數的多項式裡驗算
# =============================================================================
def part_polynomial(scene):
    exp = sorted(((nu, c) for nu, c in CH5_S21_SQUARED.items() if len(nu) <= M), reverse=True)
    gone = [nu for nu in sorted(CH5_S21_SQUARED, reverse=True) if len(nu) > M]
    p0 = mixed("換成多項式：只用 ", f"$m={M}$", " 個變數 ", "$x_1,x_2,x_3$", font_size=26)
    p1, hl1 = sum_row(r"s_{(2,1)}^2", exp, "s", fs=42)
    p2 = mixed("$" + "=".join(f"s_{{{tuple_str(nu)}}}" for nu in gone) + "=0$", "：列數超過 3", font_size=22,
               color=MUTED_COLOR)
    nums = [hook_content_count(nu, M) for nu, _ in exp]
    pieces = [Tex(f"{S21_AT_1}\\times {S21_AT_1}={S21_AT_1 ** 2}=", font_size=40)]
    num_mobs, coef_mobs = [], []
    for k, ((nu, c), v) in enumerate(zip(exp, nums)):
        if k:
            pieces.append(Tex("+", font_size=40))
        num = Tex(str(v), font_size=40)
        num_mobs.append(num)
        if c == 1:
            pieces.append(num)
        else:
            coef = Tex(f"{c}", font_size=40, fill_color=YELLOW)
            coef_mobs.append(coef)
            pieces.append(VGroup(coef, Tex(r"\cdot", font_size=40), num).arrange(RIGHT, buff=0.06))
    p3 = VGroup(*pieces).arrange(RIGHT, buff=0.2)
    labels = VGroup(*[Tex(tuple_str(nu), font_size=18, fill_color=MUTED_COLOR).next_to(m, DOWN, buff=0.15)
                      for (nu, _), m in zip(exp, num_mobs)])
    for lab in labels:
        lab.set_y(labels[0].get_y())
    sub = mixed("代入 ", "$x_1=x_2=x_3=1$", "：每項＝數字不超過 3 的表的個數", font_size=22)
    block = VGroup(p0, p1, p2, sub, VGroup(p3, labels)).arrange(DOWN, buff=0.35)
    block.move_to([0, 0.1, 0])
    p0.shift(0.1 * UP)
    assert sum(c * v for (_, c), v in zip(exp, nums)) == S21_AT_1 ** 2
    assert_in_frame(p0, p1, p2, sub, p3, labels)
    for a, b in ((p0, p1), (p1, p2), (p2, sub), (sub, VGroup(p3, labels))):
        assert_apart(a, b, gap=0.12)
    for a, b in zip(labels, labels[1:]):
        assert_apart(a, b, gap=0.12)

    scene.say("回到多項式：取 ", f"$m={M}$", " 個變數，把 ", "$s_{(2,1)}^2$", f" 真的乘開，有 {N_MONO} 種單項式")
    scene.play(FadeIn(p0), run_time=0.6)
    scene.wait(0.6)
    scene.say("從最大的單項式開始，一層層扣掉 Schur 多項式：")
    scene.play(FadeIn(p1, shift=0.1 * UP), run_time=1.0)
    scene.play(*[Indicate(t, color=YELLOW) for t in hl1], run_time=0.8)
    scene.wait(0.8)
    scene.say("係數同樣是 2；四列的形狀在 3 個變數下是 0，自動消失")
    scene.play(FadeIn(p2), run_time=0.6)
    scene.wait(1.4)
    scene.say("再全部代 1 對帳：", f"${S21_AT_1}\\times {S21_AT_1}={S21_AT_1 ** 2}$", "，右邊加起來也是 ",
              f"${S21_AT_1 ** 2}$")
    scene.play(FadeIn(sub), run_time=0.6)
    scene.play(FadeIn(p3, shift=0.1 * UP), FadeIn(labels), run_time=1.0)
    scene.wait(0.6)
    scene.say("兩邊對得上：", "$s_{(3,2,1)}$", " 的係數 2 經得起檢驗")
    scene.play(*[Indicate(t, color=YELLOW) for t in coef_mobs + hl1], run_time=0.9)
    scene.wait(2.4)


class SceneF21LRSymmetry(ChuScene):
    def construct(self):
        self.show_header("LR 數的對稱性與推論")
        check_math()
        part_faces(self)
        self.clear_stage()
        part_stuck(self)
        self.clear_stage()
        part_corollaries(self)
        self.clear_stage()
        part_polynomial(self)
        self.wait(1.0)
