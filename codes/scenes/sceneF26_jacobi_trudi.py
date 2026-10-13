"""
Scene F26 —— Schur 多項式的三個公式與主特殊化（Fulton《Young Tableaux》§6.1，書 p.75–76）

    鉤子「三條路通羅馬」：(5) h 的行列式、(6) e 的行列式、(7) 兩個交錯式相除，都通到 s_λ
    (5) Jacobi–Trudi：λ = (2,1)，矩陣下標 λ_i + j − i = [[2,3],[0,1]] → s(2,1) = h2h1 − h3；
        m 座標 (1,2,3) − (1,1,1) = (0,1,2)
    (6) 對偶：λ = (3)、λ̃ = (1,1,1)，3×3 → e1³ − 2e1e2 + e3 = h3；(2,1) 轉置不變 → s(2,1) = e2e1 − e3
    (7) m = 2：a(3,1)/a(1,0) = (x1³x2 − x1x2³)/(x1 − x2) = x1²x2 + x1x2²；m = 3：a(4,2,0)/a(2,1,0) = s(2,1)
    代入 1, q, q²：8 個表依 q 的次方分堆 → q + 2q² + 2q³ + 2q⁴ + q⁵；
        練習 5 的乘積 q·(q²−1)/(q−1)·(q⁴−1)/(q²−1)·(q²−1)/(q−1)；q = 1（練習 6）：2·2·2 = 8 = d_(2,1)(3)

數字全部由 utils/tableaux.py 算出並 assert（多項式 = {指數 tuple: 係數}）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF26_jacobi_trudi.py SceneF26JacobiTrudi
"""
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    alternant,
    complete_h,
    conjugate,
    e_lambda,
    h_lambda,
    hook_content_count,
    jacobi_trudi,
    monomial_sym,
    poly_mul,
    poly_scale,
    poly_sum,
    principal_specialization,
    schur_poly,
    ssyt,
)

M = 3
PARTS = ((3,), (2, 1), (1, 1, 1))
LAM = (2, 1)
JT_IDX = ((2, 3), (0, 1))                                   # λ_i + j − i
DUAL_LAM = (3,)
DUAL_IDX = ((1, 2, 3), (0, 1, 2), (-1, 0, 1))               # λ̃ = (1,1,1)
DUAL_COEFFS = {(1, 1, 1): 1, (2, 1): -2, (3,): 1}           # e1³ − 2 e1 e2 + e3
SELF_DUAL = {(2, 1): 1, (3,): -1}                           # s(2,1) = e2 e1 − e3
H21_M, H3_M, S21_M = (1, 2, 3), (1, 1, 1), (0, 1, 2)        # 用 m_(3), m_(2,1), m_(1,1,1) 的座標
E111_M, E21_M, E3_M = (1, 3, 6), (0, 1, 3), (0, 0, 1)
DELTA2, LD2 = (1, 0), (3, 1)
DELTA3, LD3 = (2, 1, 0), (4, 2, 0)
PS = {1: 1, 2: 2, 3: 2, 4: 2, 5: 1}                          # s(2,1)(1, q, q²)
PS_R = 1
PAIRS = ((1, 2, 2, 1), (1, 3, 4, 2), (2, 3, 2, 1))           # (i, j, λ_i − λ_j + j − i, j − i)
N_TABS = 8

H_COL, E_COL, A_COL, S_COL = BLUE, TEAL, PURPLE_B, YELLOW


def m_coeffs(f):
    return tuple(f.get(tuple(mu) + (0,) * (M - len(mu)), 0) for mu in PARTS)


def combo(fn, coeffs, m=M):
    return poly_sum(poly_scale(fn(lam, m), c) for lam, c in coeffs.items())


def weight(T):
    """x_1 → 1、x_2 → q、x_3 → q²：表 T 變成 q 的幾次方。"""
    return sum(v - 1 for row in T for v in row)


def qpoly(d):
    """{次數: 係數} → 一個變數的多項式（指數 tuple 長度 1）。"""
    return {(k,): c for k, c in d.items() if c}


def q_minus_one(a):
    return {(a,): 1, (0,): -1}


def mono_tex(e, var="x"):
    return "".join(f"{var}_{i + 1}" + (f"^{a}" if a > 1 else "") for i, a in enumerate(e) if a) or "1"


def spoly_tex(f):
    """有正負號的多項式：同型排在一起、字典序由大到小。"""
    keys = sorted(f, key=lambda e: (tuple(sorted(e, reverse=True)), e), reverse=True)
    out = ""
    for k, e in enumerate(keys):
        c = f[e]
        sign = "-" if c < 0 else ("" if k == 0 else "+")
        out += sign + ("" if abs(c) == 1 else str(abs(c))) + mono_tex(e)
    return out


def qpow(n):
    return "1" if n == 0 else ("q" if n == 1 else f"q^{{{n}}}")


def q_tex(d):
    return "+".join(("" if c == 1 else str(c)) + qpow(k) for k, c in sorted(d.items()))


def vec(v):
    return "(" + ",".join(map(str, v)) + ")"


def check_math():
    assert tuple(tuple(LAM[i] + j - i for j in range(2)) for i in range(2)) == JT_IDX
    s21 = schur_poly(LAM, M)
    assert jacobi_trudi(LAM, M) == s21 == poly_sum([h_lambda((2, 1), M), poly_scale(complete_h(3, M), -1)])
    assert m_coeffs(h_lambda((2, 1), M)) == H21_M and m_coeffs(complete_h(3, M)) == H3_M
    assert m_coeffs(s21) == S21_M == tuple(a - b for a, b in zip(H21_M, H3_M))
    lt = conjugate(DUAL_LAM)
    assert lt == (1, 1, 1) and tuple(tuple(lt[i] + j - i for j in range(3)) for i in range(3)) == DUAL_IDX
    assert jacobi_trudi(DUAL_LAM, M, dual=True) == schur_poly(DUAL_LAM, M) == complete_h(3, M)
    assert combo(e_lambda, DUAL_COEFFS) == complete_h(3, M)
    assert (m_coeffs(e_lambda((1, 1, 1), M)), m_coeffs(e_lambda((2, 1), M)), m_coeffs(e_lambda((3,), M))) == \
        (E111_M, E21_M, E3_M)
    assert tuple(a - 2 * b + c for a, b, c in zip(E111_M, E21_M, E3_M)) == H3_M
    assert conjugate(LAM) == LAM and jacobi_trudi(LAM, M, dual=True) == s21 == combo(e_lambda, SELF_DUAL)
    # (7)
    assert tuple(a + b for a, b in zip(LAM, DELTA2)) == LD2
    assert poly_mul(schur_poly(LAM, 2), alternant(DELTA2, 2)) == alternant(LD2, 2)
    assert tuple(a + b for a, b in zip(LAM + (0,), DELTA3)) == LD3
    assert poly_mul(s21, alternant(DELTA3, 3)) == alternant(LD3, 3)
    assert len(ssyt(LAM, 2)) == 2
    # 代入 1, q, q²
    tabs = ssyt(LAM, M)
    assert principal_specialization(LAM, M) == PS == dict(Counter(weight(T) for T in tabs))
    assert len(tabs) == N_TABS == sum(PS.values()) == hook_content_count(LAM, M)
    lam3 = LAM + (0,)
    assert PS_R == sum(i * a for i, a in enumerate(lam3))
    assert PAIRS == tuple((i + 1, j + 1, lam3[i] - lam3[j] + j - i, j - i) for i in range(3) for j in range(i + 1, 3))
    left, right = qpoly({PS_R: 1}), qpoly(PS)
    for _, _, a, b in PAIRS:
        left, right = poly_mul(left, q_minus_one(a)), poly_mul(right, q_minus_one(b))
    assert left == right
    prod = Fraction(1)
    for _, _, a, b in PAIRS:
        prod *= Fraction(a, b)
    assert prod == N_TABS


def det_mob(texs, cw=0.9, rh=0.6, font_size=34, color=WHITE):
    """行列式：VGroup(格子[列][欄], 左右直線)。"""
    grid = VGroup()
    for i, row in enumerate(texs):
        grid.add(VGroup(*[Tex(t, font_size=font_size, fill_color=color).move_to([j * cw, -i * rh, 0])
                          for j, t in enumerate(row)]))
    h = len(texs) * rh
    c = grid.get_center()
    xl = c[0] - len(texs[0]) * cw / 2
    bars = VGroup(*[Line([x, c[1] + h / 2, 0], [x, c[1] - h / 2, 0], stroke_color=GREY_B, stroke_width=2.5)
                    for x in (xl, xl + len(texs[0]) * cw)])
    return VGroup(grid, bars)


# =============================================================================
# 第 1 段：三條路通羅馬
# =============================================================================
def part_roads(scene):
    goal = Circle(radius=1.0).set_stroke(S_COL, width=4).set_fill(S_COL, opacity=0.12).move_to([3.6, 0.3, 0])
    goal_lab = Tex(r"s_\lambda", font_size=64, fill_color=S_COL).move_to(goal)
    defn = mixed("定義：所有表的 ", "$x^T$", " 加起來", font_size=24, color=MUTED_COLOR).next_to(goal, DOWN, buff=0.3)
    roads = VGroup()
    specs = (("(5)  ", "$h$", " 排成的行列式", H_COL), ("(6)  ", "$e$", " 排成的行列式", E_COL),
             ("(7)  兩個交錯式相除", None, None, A_COL))
    for k, (a, b, c, col) in enumerate(specs):
        txt = mixed(a, b, c, font_size=28) if b else mixed(a, font_size=28)
        box = SurroundingRectangle(txt, buff=0.2, color=col, stroke_width=3)
        roads.add(VGroup(box, txt).move_to([-3.4, 1.8 - 1.5 * k, 0]))
    arrows = VGroup(*[Arrow(r.get_right(), goal.get_center() + 1.05 * normalize(r.get_right() - goal.get_center()),
                            buff=0.1, stroke_width=5).set_color(r[0].get_color()) for r in roads])
    assert_in_frame(goal, defn, roads)
    assert_apart(roads, goal, gap=0.8)
    for a, b in zip(roads, roads[1:]):
        assert_apart(a, b, gap=0.3)

    scene.say("Schur 多項式的定義是「數表」，可是還有三個長得完全不同的公式")
    scene.play(FadeIn(goal), FadeIn(goal_lab, scale=1.3), FadeIn(defn), run_time=0.8)
    scene.wait(1.2)
    scene.say("三條路通羅馬：起點不同，終點都是 ", "$s_\\lambda$")
    for r, a in zip(roads, arrows):
        scene.play(FadeIn(r, shift=0.2 * RIGHT), GrowArrow(a), run_time=0.9)
    scene.play(Indicate(goal_lab, color=S_COL), run_time=0.8)
    scene.wait(1.6)


# =============================================================================
# 第 2 段：(5) Jacobi–Trudi 與 (6) 對偶
# =============================================================================
def jt_entry(letter, k):
    return "0" if k < 0 else ("1" if k == 0 and letter == "e" else f"{letter}_{k}")


def part_jt(scene):
    f5 = Tex(r"(5)\quad s_\lambda=\det\big(h_{\lambda_i+j-i}\big)", font_size=32, fill_color=H_COL)
    f5.move_to([-3.4, 2.6, 0])
    lam_lab = Tex(r"\lambda=" + tuple_str(LAM), font_size=26).move_to([-5.85, 1.55, 0])
    diag = YoungDiagramMob(LAM, cell_size=0.32, center=np.array([-5.85, 0.85, 0.0]))
    left = det_mob([[jt_entry("h", k) for k in row] for row in JT_IDX], cw=1.1, rh=0.8, font_size=38)
    left.move_to([-3.0, 0.85, 0])
    G = left[0]
    up = Arrow(G[0][0].get_top() + 0.15 * UP, G[0][1].get_top() + 0.15 * UP, buff=0.1, stroke_width=3)
    up_lab = Tex("+1", font_size=24, fill_color=YELLOW).next_to(up, UP, buff=0.05)
    dn = Arrow(G[1][1].get_bottom() + 0.15 * DOWN, G[1][0].get_bottom() + 0.15 * DOWN, buff=0.1, stroke_width=3)
    dn_lab = Tex("-1", font_size=24, fill_color=YELLOW).next_to(dn, DOWN, buff=0.05)
    h0 = Tex("h_0=1", font_size=26, fill_color=MUTED_COLOR).next_to(left, RIGHT, buff=0.3)
    res5 = Tex(r"s_{(2,1)}=h_2h_1-h_3", font_size=36, fill_color=S_COL).move_to([-3.4, -0.85, 0])
    chk5 = mixed("$m$", " 座標：", f"${vec(H21_M)}-{vec(H3_M)}={vec(S21_M)}$", font_size=22).move_to([-3.4, -1.65, 0])

    f6 = Tex(r"(6)\quad s_\lambda=\det\big(e_{\tilde\lambda_i+j-i}\big)", font_size=32, fill_color=E_COL)
    f6.move_to([3.4, 2.6, 0])
    lt_lab = Tex(r"\lambda=(3),\ \tilde\lambda=" + tuple_str(conjugate(DUAL_LAM)), font_size=26).move_to([3.4, 1.85, 0])
    right = det_mob([[jt_entry("e", k) for k in row] for row in DUAL_IDX], cw=0.85, rh=0.6, font_size=34)
    right.move_to([3.4, 0.55, 0])
    R = right[0]
    zeros = [R[i][j] for i in range(3) for j in range(3) if DUAL_IDX[i][j] <= 0]
    for t in zeros:
        t.set_fill(GREY_B)
    coef_str = "".join(("" if k == 0 else ("+" if c > 0 else "-")) + ("" if abs(c) == 1 else str(abs(c)))
                       + {(1, 1, 1): "e_1^3", (2, 1): "e_1e_2", (3,): "e_3"}[lam]
                       for k, (lam, c) in enumerate(DUAL_COEFFS.items()))
    res6 = Tex(r"s_{(3)}=" + coef_str + "=h_3", font_size=36, fill_color=S_COL).move_to([3.4, -0.85, 0])
    chk6 = mixed("$m$", " 座標：", f"${vec(E111_M)}-2{vec(E21_M)}+{vec(E3_M)}={vec(H3_M)}$",
                 font_size=22).move_to([3.4, -1.65, 0])
    bonus = mixed("$(2,1)$", " 轉置不變，所以也有 ", "$s_{(2,1)}=e_2e_1-e_3$", font_size=24,
                  color=OK_COLOR).move_to(2.5 * DOWN)
    L = VGroup(f5, lam_lab, diag, left, up, up_lab, dn, dn_lab, h0, res5, chk5)
    Rg = VGroup(f6, lt_lab, right, res6, chk6)
    assert_in_frame(L, Rg, bonus)
    assert_apart(L, Rg, gap=0.3)
    assert_apart(VGroup(L, Rg), bonus, gap=0.15)
    assert_apart(f5, VGroup(up, up_lab), gap=0.1)
    assert_apart(VGroup(lam_lab, diag), left, gap=0.2)
    assert_apart(VGroup(dn, dn_lab), res5, gap=0.1)
    assert_apart(lt_lab, right, gap=0.1)
    assert_apart(right, res6, gap=0.15)

    scene.say("第一條路 (5)：把 ", "$h$", " 排成方陣取行列式（Jacobi–Trudi）")
    scene.play(FadeIn(f5, shift=0.1 * DOWN), run_time=0.7)
    scene.play(FadeIn(lam_lab), FadeIn(diag), ShowCreation(left[1]), run_time=0.6)
    scene.say("對角線依序放 ", "$h_{\\lambda_1},h_{\\lambda_2}$")
    scene.play(*[FadeIn(G[i][i].set_fill(YELLOW), scale=1.3) for i in range(2)], run_time=0.7)
    scene.wait(1.0)
    scene.say("往右走一格下標加 1，往左走一格減 1")
    scene.play(GrowArrow(up), FadeIn(up_lab), FadeIn(G[0][1]), run_time=0.7)
    scene.play(GrowArrow(dn), FadeIn(dn_lab), FadeIn(G[1][0]), FadeIn(h0), run_time=0.7)
    scene.wait(0.9)
    scene.say("展開：主對角線減副對角線")
    scene.play(FadeIn(res5, shift=0.15 * DOWN), run_time=0.7)
    scene.wait(1.0)
    scene.say("用單項式座標驗算：相減剛好是 ", "$s_{(2,1)}$", " 的 ", f"${vec(S21_M)}$")
    scene.play(FadeIn(chk5), run_time=0.6)
    scene.wait(1.6)
    scene.say("第二條路 (6)：換成 ", "$e$", "，形狀也換成轉置 ", "$\\tilde\\lambda$")
    scene.play(FadeIn(f6, shift=0.1 * DOWN), FadeIn(lt_lab), run_time=0.7)
    scene.play(ShowCreation(right[1]), *[FadeIn(R[i][i].set_fill(YELLOW), scale=1.3) for i in range(3)], run_time=0.7)
    scene.say("同樣的規則；", "$e_0=1$", "，下標是負的就放 0")
    scene.play(LaggedStart(*[FadeIn(R[i][j]) for i in range(3) for j in range(3) if i != j], lag_ratio=0.1),
               run_time=0.9)
    scene.wait(0.9)
    scene.say("展開 3×3 行列式，得到的正是 ", "$h_3=s_{(3)}$")
    scene.play(FadeIn(res6, shift=0.15 * DOWN), run_time=0.7)
    scene.play(FadeIn(chk6), run_time=0.6)
    scene.wait(1.6)
    scene.say("$(2,1)$", " 的轉置還是自己：把 ", "$h$", " 全換成 ", "$e$", " 也對")
    scene.play(FadeIn(bonus, shift=0.1 * UP), run_time=0.7)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：(7) 雙交錯式
# =============================================================================
def part_bialternant(scene):
    f7 = Tex(r"(7)\quad s_\lambda=\frac{a_{\lambda+\delta}}{a_\delta}", font_size=40, fill_color=A_COL)
    defs = VGroup(Tex(r"a_{(\ell_1,\dots,\ell_m)}=\det\big(x_j^{\ell_i}\big)", font_size=30),
                  Tex(r"\delta=(m-1,\dots,1,0)", font_size=30)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    VGroup(f7, defs).arrange(RIGHT, buff=1.4).move_to(2.45 * UP)
    ex = Tex(rf"m=2,\ \lambda={tuple_str(LAM)}:\quad\lambda+\delta={tuple_str(LD2)},\ \delta={tuple_str(DELTA2)}",
             font_size=30).move_to(1.25 * UP)

    def xs_row(ell):
        return [mono_tex(tuple(ell if k == j else 0 for k in range(2))) for j in range(2)]
    num = det_mob([xs_row(l) for l in LD2], cw=0.95, rh=0.55, font_size=32)
    den = det_mob([xs_row(l) for l in DELTA2], cw=0.95, rh=0.55, font_size=32)
    w = max(num.get_width(), den.get_width()) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3)
    num.next_to(bar, UP, buff=0.15)
    den.next_to(bar, DOWN, buff=0.15)
    dets = VGroup(num, bar, den)
    eq1 = Tex("=", font_size=40)
    pfrac = Tex(r"\frac{" + spoly_tex(alternant(LD2, 2)) + "}{" + spoly_tex(alternant(DELTA2, 2)) + "}", font_size=40)
    eq2 = Tex("=", font_size=40)
    quot = Tex(spoly_tex(schur_poly(LAM, 2)), font_size=40)
    line = VGroup(dets, eq1, pfrac, eq2, quot).arrange(RIGHT, buff=0.3).move_to(0.45 * DOWN)
    final = Tex(r"=s_{(2,1)}(x_1,x_2)", font_size=40, fill_color=S_COL).next_to(quot, DOWN, buff=0.35, aligned_edge=LEFT)
    m3 = mixed("三個變數也成立：", f"$a_{{{tuple_str(LD3)}}}/a_{{{tuple_str(DELTA3)}}}=s_{{(2,1)}}(x_1,x_2,x_3)$",
               font_size=24, color=MUTED_COLOR).move_to(2.55 * DOWN)
    assert_in_frame(f7, defs, ex, line, final, m3)
    assert_apart(VGroup(f7, defs), ex, gap=0.2)
    assert_apart(ex, line, gap=0.15)
    assert_apart(line, m3, gap=0.15)
    assert_apart(final, m3, gap=0.15)
    assert_apart(dets, final, gap=0.2)

    scene.say("第三條路 (7)：交錯式 ", "$a$", " 交換兩個變數就變號")
    scene.play(FadeIn(f7, shift=0.1 * DOWN), FadeIn(defs), run_time=0.8)
    scene.wait(1.4)
    scene.say("用兩個變數試：分子、分母都是 2×2 行列式")
    scene.play(FadeIn(ex), run_time=0.5)
    scene.play(FadeIn(num), ShowCreation(bar), FadeIn(den), run_time=0.8)
    scene.wait(1.0)
    scene.say("展開後相除：分母 ", "$x_1-x_2$", " 剛好整除分子")
    scene.play(FadeIn(eq1), FadeIn(pfrac, shift=0.15 * RIGHT), run_time=0.7)
    scene.play(FadeIn(eq2), FadeIn(quot, shift=0.15 * RIGHT), run_time=0.7)
    scene.wait(1.0)
    scene.say("正是兩個表 11/2、12/2 給的 ", "$s_{(2,1)}(x_1,x_2)$")
    scene.play(FadeIn(final, shift=0.1 * DOWN), run_time=0.6)
    scene.play(FadeIn(m3), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 4 段：代入 1, q, q²
# =============================================================================
def part_spec_tableaux(scene):
    title = Tex(r"s_{(2,1)}(1,q,q^2):\quad x_1\mapsto 1,\ x_2\mapsto q,\ x_3\mapsto q^2", font_size=34)
    title.move_to(2.6 * UP)
    tabs = ssyt(LAM, M)
    mobs = VGroup(*[tableau_mob(T, 0.4) for T in tabs]).arrange(RIGHT, buff=0.5).move_to(1.5 * UP)
    wts = VGroup(*[Tex(qpow(weight(T)), font_size=30, fill_color=YELLOW).next_to(t, DOWN, buff=0.2)
                   .set_y(0.75) for T, t in zip(tabs, mobs)])
    bin_x = {d: -4.6 + 2.3 * (d - 1) for d in PS}
    targets, seen = [], Counter()
    for T, t in zip(tabs, mobs):
        d = weight(T)
        k, n = seen[d], PS[d]
        seen[d] += 1
        targets.append(np.array([bin_x[d] + (k - (n - 1) / 2) * 1.0, -0.45, 0]))
    terms = VGroup(*[Tex(("" if PS[d] == 1 else str(PS[d])) + qpow(d), font_size=34, fill_color=YELLOW)
                     .move_to([bin_x[d], -1.3, 0]) for d in PS])
    plus = VGroup(*[Tex("+", font_size=34).move_to([(bin_x[d] + bin_x[d + 1]) / 2, -1.3, 0]) for d in list(PS)[:-1]])
    total = Tex(r"s_{(2,1)}(1,q,q^2)=" + q_tex(PS), font_size=38, fill_color=S_COL).move_to(2.3 * DOWN)
    moved = VGroup(*[t.copy().move_to(p) for t, p in zip(mobs, targets)])
    assert_in_frame(title, mobs, wts, moved, terms, total)
    assert_apart(title, mobs, gap=0.2)
    assert_apart(mobs, wts, gap=0.05)
    assert_apart(wts, moved, gap=0.2)
    assert_apart(moved, terms, gap=0.15)
    assert_apart(terms, total, gap=0.2)
    for a, b in zip(moved, moved[1:]):
        assert_apart(a, b, gap=0.1)

    scene.say("換個玩法：把變數換成 ", "$1,q,q^2$", "，每個表變成 ", "$q$", " 的某個次方")
    scene.play(FadeIn(title, shift=0.1 * DOWN), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(t, shift=0.1 * DOWN) for t in mobs], lag_ratio=0.1), run_time=1.0)
    scene.say("數字 2 貢獻一個 ", "$q$", "，數字 3 貢獻 ", "$q^2$")
    scene.play(LaggedStart(*[FadeIn(w) for w in wts], lag_ratio=0.1), run_time=0.9)
    scene.wait(1.2)
    scene.say("依次方分堆：", f"${N_TABS}$", " 個表落進 5 堆")
    scene.play(FadeOut(wts), *[t.animate.move_to(p) for t, p in zip(mobs, targets)], run_time=1.4)
    scene.play(LaggedStart(*[FadeIn(t, shift=0.1 * UP) for t in terms], lag_ratio=0.1), FadeIn(plus), run_time=0.9)
    scene.wait(0.9)
    scene.say("係數 1、2、2、2、1 左右對稱")
    scene.play(FadeIn(total, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.8)


def part_spec_formula(scene):
    gen = Tex(r"s_\lambda(1,q,\dots,q^{m-1})=q^{r}\prod_{i<j}\frac{q^{\lambda_i-\lambda_j+j-i}-1}{q^{j-i}-1}",
              font_size=34)
    r_def = Tex(r"r=\lambda_2+2\lambda_3+\cdots", font_size=28, fill_color=MUTED_COLOR)
    lab = zh("練習 5", font_size=24, color=MUTED_COLOR)
    VGroup(lab, gen, r_def).arrange(RIGHT, buff=0.4).move_to(2.4 * UP)
    facs = "".join(r"\cdot\frac{" + qpow(a) + "-1}{" + qpow(b) + "-1}" for _, _, a, b in PAIRS)
    inst = Tex(r"s_{(2,1)}(1,q,q^2)=" + qpow(PS_R) + facs, font_size=38).move_to(1.0 * UP)
    inst2 = Tex("=" + q_tex(PS), font_size=38, fill_color=S_COL).next_to(inst, DOWN, buff=0.3)
    inst2.align_to(inst[0], LEFT).shift(2.2 * RIGHT)
    vals = r"\cdot".join(rf"\frac{{{a}}}{{{b}}}" for _, _, a, b in PAIRS)
    q1 = Tex(r"q=1:\quad " + vals + f"={N_TABS}", font_size=38, fill_color=YELLOW).move_to(1.05 * DOWN)
    why = VGroup(mixed("＝前一頁的 ", f"${N_TABS}$", " 個表（練習 6）", font_size=24),
                 mixed("＝鉤–內容公式 ", f"$d_{{(2,1)}}(3)={hook_content_count(LAM, M)}$", "（第 4 章）",
                       font_size=24)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(q1, DOWN, buff=0.35)
    assert_in_frame(lab, gen, r_def, inst, inst2, q1, why)
    assert_apart(VGroup(lab, gen, r_def), inst, gap=0.2)
    assert_apart(inst, inst2, gap=0.1)
    assert_apart(inst2, q1, gap=0.2)
    assert_apart(q1, why, gap=0.1)

    scene.say("不必數表也行：", "$r$", " 加上一串分式的乘積（練習 5）")
    scene.play(FadeIn(VGroup(lab, gen, r_def), shift=0.1 * DOWN), run_time=0.8)
    scene.wait(1.6)
    scene.say("$\\lambda=(2,1,0)$", "：三對 ", "$i<j$", "，三個分式")
    scene.play(FadeIn(inst, shift=0.15 * RIGHT), run_time=0.8)
    scene.wait(1.2)
    scene.say("約分、乘開，和數表的結果一模一樣")
    scene.play(FadeIn(inst2, shift=0.1 * DOWN), run_time=0.7)
    scene.wait(1.3)
    scene.say("再令 ", "$q=1$", "：每個分式變成一個分數，乘起來是表的個數")
    scene.play(FadeIn(q1, shift=0.1 * UP), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(w, shift=0.1 * RIGHT) for w in why], lag_ratio=0.4), run_time=1.0)
    scene.wait(2.2)


class SceneF26JacobiTrudi(ChuScene):
    def construct(self):
        self.show_header("Schur 多項式的三個公式")
        check_math()
        part_roads(self)
        self.clear_stage()
        part_jt(self)
        self.clear_stage()
        part_bialternant(self)
        self.clear_stage()
        part_spec_tableaux(self)
        self.clear_stage()
        part_spec_formula(self)
        self.wait(1.0)
