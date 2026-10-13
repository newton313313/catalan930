"""
Scene F25 —— 對稱多項式的五組基底（Fulton《Young Tableaux》§6.1，書 p.72–74）

    鉤子「五種語言說同一件事」：f = h_2 h_1（3 個變數）用 m、s、e、h、p 五組基底寫出來
    命題 1：n = 3 的轉換矩陣（每列 = 用 m_μ 寫出的係數）——s 上三角（首項 x^λ）、e 反對角（首項 x^λ̃）、
        h 的 det = 1、p 的對角線 1, 1, 6（det = 6，要有理係數）
    E(−t)H(t) = 1 → Σ(−1)^i e_i h_{k−i} = 0；k = 3 時三個單項式的係數 1−1、1−2+1、1−3+3−1 都是 0
    Newton：k h_k = p_1 h_{k−1} + … + p_k（k = 1, 2, 3）→ h_3 = Σ p_λ / z(λ)；z = 3, 2, 6，
        3!/z(λ) = S_3 中循環型為 λ 的排列個數 2, 3, 1

數字全部由 utils/tableaux.py 算出並 assert（多項式 = {指數 tuple: 係數}，m = 3 個變數）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF25_bases.py SceneF25Bases
"""
import sys
from collections import Counter
from fractions import Fraction
from itertools import permutations
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tuple_str
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    complete_h,
    e_lambda,
    elementary_e,
    h_lambda,
    monomial_sym,
    p_lambda,
    partitions,
    poly_mul,
    poly_scale,
    poly_sum,
    power_sum,
    schur_poly,
    z_lambda,
)

M = 3
PARTS = ((3,), (2, 1), (1, 1, 1))
F_SHAPE = (2, 1)                                             # f = h_2 h_1
LANGS = (                                                    # (名稱, 字母, 顏色, f 的係數 {λ: c})
    ("單項式", "m", GREY_A, {(3,): 1, (2, 1): 2, (1, 1, 1): 3}),
    ("Schur", "s", YELLOW, {(3,): 1, (2, 1): 1}),
    ("基本", "e", TEAL, {(1, 1, 1): 1, (2, 1): -1}),
    ("完全", "h", BLUE, {(2, 1): 1}),
    ("冪和", "p", PINK, {(1, 1, 1): Fraction(1, 2), (2, 1): Fraction(1, 2)}),
)
COLORS = {letter: col for _, letter, col, _ in LANGS}
MATS = {"s": ((1, 1, 1), (0, 1, 2), (0, 0, 1)), "e": ((0, 0, 1), (0, 1, 3), (1, 3, 6)),
        "h": ((1, 1, 1), (1, 2, 3), (1, 3, 6)), "p": ((1, 0, 0), (1, 1, 0), (1, 3, 6))}
DETS = {"s": 1, "e": -1, "h": 1, "p": 6}
EH_MONOS = ((3, 0, 0), (2, 1, 0), (1, 1, 1))
EH_TABLE = ((1, -1, 0, 0), (1, -2, 1, 0), (1, -3, 3, -1))      # 單項式在 (−1)^i e_i h_{3−i} 裡的係數
NEWTON_H = {1: {(1,): 1}, 2: {(1, 1): Fraction(1, 2), (2,): Fraction(1, 2)},
            3: {(1, 1, 1): Fraction(1, 6), (2, 1): Fraction(1, 2), (3,): Fraction(1, 3)}}
Z_ROWS = ((1, 1, 1), (2, 1), (3,))                           # z 表的列順序
Z_VALUES = {(1, 1, 1): 6, (2, 1): 2, (3,): 3}
CLASSES = {(1, 1, 1): (r"\mathrm{id}",), (2, 1): ("(12)", "(13)", "(23)"), (3,): ("(123)", "(132)")}


def basis(letter, lam, m=M):
    return {"m": monomial_sym, "s": schur_poly, "e": e_lambda, "h": h_lambda, "p": p_lambda}[letter](lam, m)


def combo(letter, coeffs, m=M):
    return poly_sum(poly_scale(basis(letter, lam, m), c) for lam, c in coeffs.items())


def m_coeffs(f):
    return tuple(f.get(tuple(mu) + (0,) * (M - len(mu)), 0) for mu in PARTS)


def det3(A):
    return sum(A[0][p[0]] * A[1][p[1]] * A[2][p[2]] * (1 if sum(p[i] > p[j] for i in range(3)
                                                              for j in range(i + 1, 3)) % 2 == 0 else -1)
               for p in permutations(range(3)))


def cycles(p):
    """排列 p（p[i] = i 的像，0 起算）的循環（1 起算），長度 1 的省略。"""
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen:
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j + 1)
            j = p[j]
        out.append(tuple(c))
    return out


def cycle_type(p):
    return tuple(sorted((len(c) for c in cycles(p)), reverse=True))


def cycle_tex(p):
    cs = [c for c in cycles(p) if len(c) > 1]
    return "".join("(" + "".join(map(str, c)) + ")" for c in cs) or r"\mathrm{id}"


def mono_tex(e, var="x"):
    return "".join(f"{var}_{i + 1}" + (f"^{a}" if a > 1 else "") for i, a in enumerate(e) if a) or "1"


def poly_terms(f):
    """[(係數, 單項式)]：同型的排在一起（型由大到小），同型內字典序由大到小。"""
    keys = sorted(f, key=lambda e: (tuple(sorted(e, reverse=True)), e), reverse=True)
    return [(f[e], mono_tex(e)) for e in keys]


def poly_tex(f, head=4, tail=1):
    terms = poly_terms(f)
    shown = terms if len(terms) <= head + tail else terms[:head] + [None] + terms[-tail:]
    out = ""
    for k, t in enumerate(shown):
        if t is None:
            out += r"+\cdots"
            continue
        c, mono = t
        out += ("" if k == 0 else "+") + ("" if c == 1 else str(c)) + mono
    return out


def coef_tex(c, first):
    sign = "-" if c < 0 else ("" if first else "+")
    c = abs(c)
    if c == 1:
        return sign
    if isinstance(c, Fraction) and c.denominator > 1:
        return sign + rf"\frac{{{c.numerator}}}{{{c.denominator}}}"
    return sign + str(c)


def combo_tex(letter, coeffs):
    return "".join(coef_tex(c, k == 0) + f"{letter}_{{{tuple_str(lam)}}}" for k, (lam, c) in enumerate(coeffs.items()))


def pprod_tex(lam):
    return "".join(f"p_{r}" + (f"^{k}" if k > 1 else "") for r, k in sorted(Counter(lam).items()))


def check_math():
    assert tuple(partitions(3)) == PARTS
    f = h_lambda(F_SHAPE, M)
    for _, letter, _, coeffs in LANGS:
        assert combo(letter, coeffs) == f, letter
    assert m_coeffs(f) == tuple(LANGS[0][3][lam] for lam in PARTS)
    for letter, A in MATS.items():
        assert tuple(m_coeffs(basis(letter, lam)) for lam in PARTS) == A and det3(A) == DETS[letter]
        for lam in PARTS:                              # m_coeffs 抓得到全部：基底元素 = Σ 係數 · m_μ
            assert combo("m", dict(zip(PARTS, m_coeffs(basis(letter, lam))))) == basis(letter, lam)
    # E(−t)H(t) = 1
    one = {(0,) * M: 1}
    for k in range(1, 4):
        terms = [poly_scale(poly_mul(elementary_e(i, M), complete_h(k - i, M)), (-1) ** i) for i in range(k + 1)]
        assert poly_sum(terms) == {}
        if k == 3:
            assert tuple(tuple(t.get(e, 0) for t in terms) for e in EH_MONOS) == EH_TABLE
    assert complete_h(0, M) == elementary_e(0, M) == one
    # Newton：k h_k = Σ p_i h_{k−i}
    for k in range(1, 4):
        assert poly_scale(complete_h(k, M), k) == poly_sum(poly_mul(power_sum(i, M), complete_h(k - i, M))
                                                          for i in range(1, k + 1))
        assert combo("p", NEWTON_H[k]) == complete_h(k, M)
    assert all(NEWTON_H[3][lam] == Fraction(1, z_lambda(lam)) == Fraction(1, Z_VALUES[lam]) for lam in Z_ROWS)
    # n!/z(λ) = 循環型 λ 的排列數
    by_type = {}
    for p in permutations(range(3)):
        by_type.setdefault(cycle_type(p), []).append(cycle_tex(p))
    for lam in Z_ROWS:
        assert tuple(sorted(by_type[lam])) == tuple(sorted(CLASSES[lam]))
        assert len(CLASSES[lam]) == factorial(3) // z_lambda(lam)
    assert sum(len(v) for v in CLASSES.values()) == factorial(3)


# =============================================================================
# 第 1 段：五種語言
# =============================================================================
def part_languages(scene):
    f = h_lambda(F_SHAPE, M)
    top = Tex("f=h_2h_1=" + poly_tex(f), font_size=36).move_to(2.6 * UP)
    rows = VGroup()
    for k, (name, letter, col, coeffs) in enumerate(LANGS):
        lab = VGroup(zh(name, font_size=26, color=col), Tex(letter, font_size=36, fill_color=col))
        lab.arrange(RIGHT, buff=0.15).move_to([-2.8, 1.45 - 0.78 * k, 0], aligned_edge=RIGHT)
        eq = Tex("f=" + combo_tex(letter, coeffs), font_size=38)
        eq.move_to([-2.2, 1.45 - 0.78 * k, 0], aligned_edge=LEFT)
        rows.add(VGroup(lab, eq))
    m_row = rows[0][1]
    note = mixed("＝", "$x_1^3$", "、", "$x_1^2x_2$", "、", "$x_1x_2x_3$", " 的係數", font_size=20,
                 color=MUTED_COLOR).next_to(m_row, RIGHT, buff=0.4)
    moral = mixed("同一個向量，五組座標", font_size=28, color=OK_COLOR).move_to(2.55 * DOWN)
    assert_in_frame(top, rows, note, moral)
    assert_apart(top, rows, gap=0.3)
    assert_apart(rows, moral, gap=0.2)
    assert_apart(m_row, note, gap=0.2)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a, b, gap=0.12)

    scene.say("同一個對稱多項式，能用五種「語言」說出來")
    scene.play(FadeIn(top, shift=0.15 * DOWN), run_time=0.8)
    scene.wait(0.8)
    scene.say("最直接的語言：數每一型單項式有幾個")
    scene.play(FadeIn(rows[0], shift=0.2 * RIGHT), run_time=0.7)
    scene.play(FadeIn(note), run_time=0.5)
    scene.wait(1.2)
    scene.say("換成 Schur、基本、完全、冪和：係數全都不一樣")
    for row in rows[1:]:
        scene.play(FadeIn(row, shift=0.2 * RIGHT), run_time=0.6)
        scene.wait(0.3)
    scene.say("冪和那一行還出現了分數 ", "$\\tfrac12$", "：先記住這個伏筆")
    scene.play(Indicate(rows[4][1], color=PINK), run_time=1.0)
    scene.wait(0.4)
    scene.say("每一種語言都是一組基底，係數就是座標")
    scene.play(FadeIn(moral, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.2)


# =============================================================================
# 第 2 段：命題 1——轉換矩陣與首項
# =============================================================================
def brackets(mob, buff=0.2, tick=0.12, color=GREY_B):
    l, r = mob.get_left()[0] - buff, mob.get_right()[0] + buff
    t, b = mob.get_top()[1] + 0.08, mob.get_bottom()[1] - 0.08
    left = VMobject().set_points_as_corners([[l + tick, t, 0], [l, t, 0], [l, b, 0], [l + tick, b, 0]])
    right = VMobject().set_points_as_corners([[r - tick, t, 0], [r, t, 0], [r, b, 0], [r - tick, b, 0]])
    return VGroup(left, right).set_stroke(color, width=2)


def coef_panel(letter, x_left, y_top, cw=0.8, rh=0.5):
    """VGroup(標題, 欄名, 數字[列][欄], 括號, det)。"""
    A = MATS[letter]
    xs = [x_left + (j + 0.5) * cw for j in range(3)]
    title = Tex(letter + r"_\lambda", font_size=38, fill_color=COLORS[letter]).move_to([xs[1], y_top - 0.2, 0])
    heads = VGroup(*[Tex(f"m_{{{tuple_str(mu)}}}", font_size=20, fill_color=MUTED_COLOR)
                     .move_to([x, y_top - 0.75, 0]) for x, mu in zip(xs, PARTS)])
    nums = VGroup(*[VGroup(*[Tex(str(v), font_size=32).move_to([x, y_top - 0.75 - (i + 1) * rh, 0])
                             for x, v in zip(xs, row)]) for i, row in enumerate(A)])
    det = Tex(rf"\det={DETS[letter]}", font_size=28).move_to([xs[1], y_top - 0.85 - 4 * rh, 0])
    return VGroup(title, heads, nums, brackets(nums), det)


def part_matrices(scene):
    y_top, rh = 2.95, 0.5
    panels = {letter: coef_panel(letter, -5.2 + 3.05 * k, y_top) for k, letter in enumerate("sehp")}
    row_labs = VGroup(*[Tex(tuple_str(lam), font_size=24, fill_color=MUTED_COLOR)
                        .move_to([-6.15, y_top - 0.75 - (i + 1) * rh, 0]) for i, lam in enumerate(PARTS)])
    lam_lab = Tex(r"\lambda", font_size=28, fill_color=MUTED_COLOR).move_to([-6.15, y_top - 0.75, 0])
    notes = VGroup(
        mixed("$s_\\lambda=m_\\lambda+$", "（較小的 ", "$m_\\mu$", "）：首項係數 1，上三角", font_size=24),
        mixed("$e_\\lambda=m_{\\tilde\\lambda}+\\cdots$", "：首項是轉置的 ", "$x^{\\tilde\\lambda}$",
              "，列倒過來也是三角", font_size=24),
        mixed("$h_\\lambda=\\sum_\\mu K_{\\mu\\lambda}\\,s_\\mu$", "：Kostka 矩陣可逆，所以也行", font_size=24),
        mixed("$p_\\lambda$", " 的對角線出現 ", "$6$", "：要除以 6，只在有理係數下是基底", font_size=24),
    ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-6.3, -0.75, 0], aligned_edge=UL)
    group = VGroup(row_labs, lam_lab, *panels.values())
    assert_in_frame(group, notes)
    assert_apart(group, notes, gap=0.2)
    assert_apart(VGroup(row_labs, lam_lab), panels["s"], gap=0.15)
    for a, b in zip("seh", "ehp"):
        assert_apart(panels[a], panels[b], gap=0.2)
    marks = {
        "s": [panels["s"][2][i][i] for i in range(3)],
        "e": [panels["e"][2][i][2 - i] for i in range(3)],
        "h": [],
        "p": [panels["p"][2][i][i] for i in range(3)],
    }

    scene.say("為什麼是基底？把每個基底元素都翻譯成單項式 ", "$m_\\mu$")
    scene.play(FadeIn(row_labs), FadeIn(lam_lab), run_time=0.5)
    for k, letter in enumerate("sehp"):
        p = panels[letter]
        scene.play(FadeIn(p[0]), FadeIn(p[1]), FadeIn(p[3]),
                   LaggedStart(*[FadeIn(t) for row in p[2] for t in row], lag_ratio=0.05), run_time=0.8)
    scene.wait(0.5)
    caps = {
        "s": ("$s_\\lambda$", " 的首項恰好是 ", "$x^\\lambda$", "、係數 1：矩陣是三角形"),
        "e": ("$e_\\lambda$", " 的首項是轉置形狀的 ", "$x^{\\tilde\\lambda}$", "：1 落在反對角線上"),
        "h": ("$h_\\lambda$", " 可以先換成 Schur 多項式，行列式也是 1"),
        "p": ("冪和的行列式是 6：整數不夠用，要允許分數",),
    }
    for k, letter in enumerate("sehp"):
        scene.say(*caps[letter])
        p = panels[letter]
        rects = VGroup(*[SurroundingRectangle(t, buff=0.07, color=COLORS[letter], stroke_width=2.5)
                         for t in marks[letter]])
        anims = [FadeIn(notes[k], shift=0.1 * UP), FadeIn(p[4])]
        if len(rects):
            anims.append(ShowCreation(rects))
        if letter == "p":
            anims.append(p[2][2][2].animate.set_fill(RED))
        scene.play(*anims, run_time=0.8)
        scene.wait(1.3)
    scene.say("命題 1：變數夠多時（", "$m\\ge n$", "），五組都是 ", "$n$", " 次對稱多項式的基底")
    scene.wait(1.5)


# =============================================================================
# 第 3 段：E(−t)H(t) = 1
# =============================================================================
def part_eh(scene):
    E = Tex(r"E(t)=\prod_{i=1}^{3}(1+x_it)=\sum_k e_kt^k", font_size=30)
    H = Tex(r"H(t)=\prod_{i=1}^{3}\frac{1}{1-x_it}=\sum_k h_kt^k", font_size=30)
    VGroup(E, H).arrange(RIGHT, buff=0.9).move_to(2.55 * UP)
    E.set_fill(TEAL)
    H.set_fill(BLUE)
    key = Tex(r"E(-t)H(t)=1", font_size=40)
    arr = Tex(r"\Longrightarrow", font_size=40)
    rel = Tex(r"\sum_{i=0}^{k}(-1)^i e_ih_{k-i}=0", font_size=38)
    line2 = VGroup(key, arr, rel).arrange(RIGHT, buff=0.4).move_to(1.25 * UP)
    xs = [-4.7, -2.7, -1.1, 0.5, 2.0, 3.6]
    heads_tex = ["h_3", "-e_1h_2", "+e_2h_1", "-e_3", r"\Sigma"]
    y_head, rh = -0.05, 0.6
    head_lab = zh("單項式", font_size=22, color=MUTED_COLOR).move_to([xs[0], y_head, 0])
    heads = VGroup(*[Tex(t, font_size=30, fill_color=MUTED_COLOR).move_to([x, y_head, 0])
                     for x, t in zip(xs[1:], heads_tex)])
    rows = VGroup()
    for r, (e, vals) in enumerate(zip(EH_MONOS, EH_TABLE)):
        y = y_head - (r + 1) * rh
        row = VGroup(Tex(mono_tex(e), font_size=32).move_to([xs[0], y, 0]))
        for x, v in zip(xs[1:5], vals):
            row.add(Tex(str(v), font_size=32, fill_color=WHITE if v else GREY_C).move_to([x, y, 0]))
        row.add(Tex(str(sum(vals)), font_size=34, fill_color=OK_COLOR).move_to([xs[5], y, 0]))
        rows.add(row)
    h_line = Line([xs[0] - 0.8, y_head - rh / 2, 0], [xs[5] + 0.5, y_head - rh / 2, 0], stroke_color=GREY_C,
                  stroke_width=2)
    v_line = Line([2.8, y_head + rh / 2, 0], [2.8, y_head - 3.5 * rh, 0], stroke_color=GREY_C, stroke_width=2)
    table = VGroup(head_lab, heads, rows, h_line, v_line)
    assert_in_frame(E, H, line2, table)
    assert_apart(E, H, gap=0.4)
    assert_apart(VGroup(E, H), line2, gap=0.25)
    assert_apart(line2, table, gap=0.25)

    scene.say("兩個生成函數：", "$E(t)$", " 收集 ", "$e_k$", "，", "$H(t)$", " 收集 ", "$h_k$")
    scene.play(FadeIn(E, shift=0.1 * DOWN), FadeIn(H, shift=0.1 * DOWN), run_time=0.8)
    scene.wait(1.0)
    scene.say("把 ", "$t$", " 換成 ", "$-t$", "：每個因子 ", "$1-x_it$", " 剛好和分母抵消")
    scene.play(FadeIn(key, shift=0.1 * UP), run_time=0.7)
    scene.wait(0.8)
    scene.say("比較 ", "$t^k$", " 的係數：", "$e$", " 和 ", "$h$", " 互相決定")
    scene.play(FadeIn(arr), FadeIn(rel, shift=0.15 * RIGHT), run_time=0.7)
    scene.wait(1.0)
    scene.say("拿 ", "$k=3$", " 驗算：看三個單項式各自的係數")
    scene.play(FadeIn(head_lab), FadeIn(heads), ShowCreation(h_line), ShowCreation(v_line), run_time=0.7)
    for row in rows:
        scene.play(LaggedStart(*[FadeIn(t) for t in row[:-1]], lag_ratio=0.12), run_time=0.7)
        scene.play(FadeIn(row[-1], scale=1.4), run_time=0.4)
    scene.say("每一列加起來都是 0：", "$1-3+3-1=0$", " 就是二項式定理")
    scene.play(*[Indicate(row[-1], color=OK_COLOR) for row in rows], run_time=0.9)
    scene.wait(1.3)


# =============================================================================
# 第 4 段：Newton 恆等式
# =============================================================================
def h_in_p_tex(k):
    return f"h_{k}=" + "".join(coef_tex(c, i == 0) + pprod_tex(lam) for i, (lam, c) in enumerate(NEWTON_H[k].items()))


def part_newton(scene):
    title = mixed("Newton 恆等式：", "$k\\,h_k=p_1h_{k-1}+p_2h_{k-2}+\\cdots+p_kh_0$", font_size=30)
    title.move_to([-6.3, 2.55, 0], aligned_edge=LEFT)
    steps = VGroup()
    for k in range(1, 4):
        y = 1.35 - 1.15 * (k - 1)
        lab = Tex(f"k={k}", font_size=32, fill_color=MUTED_COLOR).move_to([-6.2, y, 0], aligned_edge=LEFT)
        rhs = "+".join(f"p_{i}h_{k - i}" for i in range(1, k + 1))
        eq = Tex(("" if k == 1 else str(k)) + f"h_{k}=" + rhs, font_size=34).move_to([-4.9, y, 0], aligned_edge=LEFT)
        res = Tex(h_in_p_tex(k), font_size=36, fill_color=PINK)
        steps.add(VGroup(lab, eq, Tex(r"\Longrightarrow", font_size=34), res))
    x_arr = max(s[1].get_right()[0] for s in steps) + 0.55
    for s in steps:
        s[2].move_to([x_arr, s[1].get_center()[1], 0])
        s[3].move_to([x_arr + 0.55, s[1].get_center()[1], 0], aligned_edge=LEFT)
    denoms = mixed("分母 ", "$6,\\ 2,\\ 3$", " 從哪裡來？", font_size=28, color=YELLOW).move_to([2.6, -2.25, 0])
    assert_in_frame(title, steps, denoms)
    assert_apart(title, steps, gap=0.3)
    for s in steps:
        assert_apart(s[1], s[2], gap=0.1)
        assert_apart(s[2], s[3], gap=0.1)
    for a, b in zip(steps, steps[1:]):
        assert_apart(a, b, gap=0.25)
    assert_apart(steps, denoms, gap=0.15)

    scene.say("冪和 ", "$p_k=x_1^k+x_2^k+x_3^k$", " 和 ", "$h$", " 之間也有一條遞迴：Newton 恆等式")
    scene.play(FadeIn(title, shift=0.1 * DOWN), run_time=0.8)
    scene.wait(1.0)
    for k, s in enumerate(steps, start=1):
        if k == 1:
            scene.say("$k=1$", "：", "$h_0=1$", "，直接得到 ", "$h_1=p_1$")
        else:
            scene.say(f"$k={k}$", "：代入前面算好的 ", "$h$", "，解出 ", f"$h_{k}$")
        scene.play(FadeIn(s[0]), FadeIn(s[1], shift=0.15 * RIGHT), run_time=0.6)
        if k > 1:
            scene.play(Indicate(steps[k - 2][3], color=PINK), run_time=0.6)
        scene.play(FadeIn(s[2]), FadeIn(s[3], shift=0.2 * RIGHT), run_time=0.6)
        scene.wait(0.7)
    scene.say("分數又出現了：", "$\\tfrac16,\\ \\tfrac12,\\ \\tfrac13$", "，它們有什麼意義？")
    scene.play(FadeIn(denoms, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.1)


# =============================================================================
# 第 5 段：z(λ) 與 S_3 的循環型
# =============================================================================
def part_z(scene):
    lemma = Tex(r"h_n=\sum_{\lambda\vdash n}\frac{p_\lambda}{z(\lambda)}", font_size=40)
    zdef = Tex(r"z(\lambda)=\prod_r r^{m_r}\,m_r!", font_size=34)
    zsub = mixed("$m_r$", "：", "$\\lambda$", " 裡 ", "$r$", " 出現幾次", font_size=22, color=MUTED_COLOR)
    VGroup(zdef, zsub).arrange(DOWN, buff=0.15)
    VGroup(lemma, VGroup(zdef, zsub)).arrange(RIGHT, buff=1.2).move_to(2.3 * UP)
    xs = [-5.0, -3.1, -1.3, 0.6]
    y_head, rh = 0.85, 0.72
    heads = VGroup(mixed("循環型 ", "$\\lambda$", font_size=22, color=MUTED_COLOR),
                   Tex(r"z(\lambda)", font_size=30, fill_color=MUTED_COLOR),
                   Tex(r"3!/z(\lambda)", font_size=30, fill_color=MUTED_COLOR),
                   mixed("$S_3$", " 中這一型的排列", font_size=22, color=MUTED_COLOR))
    for k, (h, x) in enumerate(zip(heads, xs)):
        h.move_to([x, y_head, 0], aligned_edge=LEFT if k == 3 else ORIGIN)
    rows = VGroup()
    for r, lam in enumerate(Z_ROWS):
        y = y_head - (r + 1) * rh
        row = VGroup(Tex(tuple_str(lam), font_size=32).move_to([xs[0], y, 0]),
                     Tex(str(z_lambda(lam)), font_size=32, fill_color=PINK).move_to([xs[1], y, 0]),
                     Tex(str(factorial(3) // z_lambda(lam)), font_size=34, fill_color=YELLOW).move_to([xs[2], y, 0]),
                     Tex(r"\quad ".join(CLASSES[lam]), font_size=32).move_to([xs[3], y, 0], aligned_edge=LEFT))
        rows.add(row)
    h_line = Line([xs[0] - 0.9, y_head - rh / 2, 0], [5.6, y_head - rh / 2, 0], stroke_color=GREY_C, stroke_width=2)
    total = Tex("+".join(str(factorial(3) // z_lambda(lam)) for lam in Z_ROWS) + "=6=3!", font_size=32,
                fill_color=YELLOW).move_to([xs[2] + 0.4, y_head - 4 * rh - 0.1, 0])
    total_note = zh("每個排列恰好算一次", font_size=22, color=MUTED_COLOR).next_to(total, RIGHT, buff=0.35)
    table = VGroup(heads, rows, h_line)
    assert_in_frame(lemma, zdef, zsub, table, total, total_note)
    assert_apart(VGroup(lemma, zdef, zsub), table, gap=0.25)
    assert_apart(table, VGroup(total, total_note), gap=0.1)
    assert_apart(lemma, zdef, gap=0.5)

    scene.say("把分母寫成 ", "$z(\\lambda)$", "：", "$h_3$", " 是所有 ", "$p_\\lambda$", " 除以 ", "$z(\\lambda)$", " 的和")
    scene.play(FadeIn(lemma, shift=0.1 * DOWN), run_time=0.8)
    scene.play(FadeIn(zdef), FadeIn(zsub), run_time=0.7)
    scene.wait(1.0)
    scene.say("把 ", "$3!$", " 個排列依循環型分組，再數一數")
    scene.play(FadeIn(heads), ShowCreation(h_line), run_time=0.6)
    for row in rows:
        scene.play(FadeIn(row[0]), FadeIn(row[1]), run_time=0.4)
        scene.play(FadeIn(row[3], shift=0.15 * RIGHT), FadeIn(row[2], scale=1.3), run_time=0.6)
        scene.wait(0.5)
    scene.say("$3!/z(\\lambda)$", " 恰好是循環型為 ", "$\\lambda$", " 的排列個數：1、3、2")
    scene.play(*[Indicate(row[2], color=YELLOW) for row in rows], run_time=0.9)
    scene.play(FadeIn(total), FadeIn(total_note), run_time=0.6)
    scene.wait(1.2)
    scene.say("所以 ", "$p_\\lambda/z(\\lambda)$", " 是在對 ", "$S_n$", " 平均：第 7 章會再見到它")
    scene.wait(1.6)


class SceneF25Bases(ChuScene):
    def construct(self):
        self.show_header("對稱多項式的五組基底")
        check_math()
        part_languages(self)
        self.clear_stage()
        part_matrices(self)
        self.clear_stage()
        part_eh(self)
        self.clear_stage()
        part_newton(self)
        self.clear_stage()
        part_z(self)
        self.wait(1.0)
