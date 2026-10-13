"""
Scene F27 —— 對稱函數環 Λ、Cauchy 核、內積與 ω（Fulton《Young Tableaux》§6.2，書 p.77–78）

    鉤子「讓變數無限多」：令 x_3 = 0，s(2,1)(x1,x2,x3) 的 7 項只剩 x1²x2 + x1x2² = s(2,1)(x1,x2)；
        s(1,1,1) → 0 → Λ_{m+1} → Λ_m 相容，每個次數在 m ≥ n 時穩定 → Λ
    Cauchy 核（命題 2）：Π 1/(1 − x_i y_j) = Σ h_λ(x)m_λ(y) = Σ p_λ(x)p_λ(y)/z(λ) = Σ s_λ(x)s_λ(y)；
        次數 3 的部分在 3+3 個變數裡比對，x1x2x3y1y2y3 的係數：0+0+6、0+0+6、1+4+1（= 1²+2²+1²）
    內積（命題 3）：⟨h_λ, m_μ⟩ = δ（單位矩陣）、⟨p_λ, p_μ⟩ = z(λ)δ（對角 3, 2, 6）
    ω（推論 1）：Young 圖翻轉 (3,1) → (2,1,1)、(3) → (1,1,1)：ω(h_3) = e_3；ω(p_μ) = (−1)^{|μ|−ℓ(μ)} p_μ（+、−、+）
    預告：p_μ = Σ χ^λ_μ s_λ，n = 3 的表 [[1,1,1],[−1,0,2],[1,−1,1]]；μ = (1,1,1) 那一行 = 標準表個數 1, 2, 1

數字全部由 utils/tableaux.py 算出並 assert（多項式 = {指數 tuple: 係數}）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF27_symmetric_functions.py SceneF27SymFunctions
"""
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    character_table,
    complete_h,
    conjugate,
    elementary_e,
    h_lambda,
    monomial_sym,
    omega,
    p_lambda,
    partitions,
    poly_mul,
    poly_scale,
    poly_sum,
    schur_inner,
    schur_poly,
    standard_tableaux,
    z_lambda,
)

M = 3
PARTS = ((3,), (2, 1), (1, 1, 1))
TARGET = (1, 1, 1, 1, 1, 1)                                  # x1x2x3 y1y2y3
CONTRIB = {"h": (0, 0, 6), "p": (0, 0, 6), "s": (1, 4, 1)}
GRAM_HM = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
GRAM_PP = ((3, 0, 0), (0, 2, 0), (0, 0, 6))
FLIPS = (((3, 1), (2, 1, 1)), ((3,), (1, 1, 1)))
OMEGA_SIGN = {(3,): 1, (2, 1): -1, (1, 1, 1): 1}
CHI = ((1, 1, 1), (-1, 0, 2), (1, -1, 1))                    # 列 λ、行 μ（順序同 PARTS）
F_LAMBDA = (1, 2, 1)

H_COL, P_COL, S_COL = BLUE, PINK, YELLOW


def mono_tex(e, var="x"):
    return "".join(f"{var}_{i + 1}" + (f"^{a}" if a > 1 else "") for i, a in enumerate(e) if a) or "1"


def poly_terms(f):
    """[(指數, 項的 Tex)]：同型的排在一起（型由大到小），同型內字典序由大到小；係數都是正的。"""
    keys = sorted(f, key=lambda e: (tuple(sorted(e, reverse=True)), e), reverse=True)
    return [(e, ("" if f[e] == 1 else str(f[e])) + mono_tex(e)) for e in keys]


def xy(f, side):
    """3 個變數的多項式放進 (x1,x2,x3,y1,y2,y3)：side 0 用 x、side 1 用 y。"""
    return {(e + (0,) * M) if side == 0 else ((0,) * M + e): c for e, c in f.items()}


def cauchy_degree(n, m=M):
    """Π 1/(1 − x_i y_j) 的 n 次部分 = h_n(所有 x_i y_j)。"""
    out = {}
    for e, c in complete_h(n, m * m).items():
        key = tuple(sum(e[m * i + j] for j in range(m)) for i in range(m)) + \
            tuple(sum(e[m * i + j] for i in range(m)) for j in range(m))
        out[key] = out.get(key, 0) + c
    return out


def cauchy_terms(kind):
    """[每個 λ 的那一項]（6 個變數的多項式）。"""
    out = []
    for lam in PARTS:
        if kind == "h":
            out.append(poly_mul(xy(h_lambda(lam, M), 0), xy(monomial_sym(lam, M), 1)))
        elif kind == "p":
            out.append(poly_scale(poly_mul(xy(p_lambda(lam, M), 0), xy(p_lambda(lam, M), 1)),
                                  Fraction(1, z_lambda(lam))))
        else:
            out.append(poly_mul(xy(schur_poly(lam, M), 0), xy(schur_poly(lam, M), 1)))
    return out


def check_math():
    assert tuple(partitions(3)) == PARTS
    # x_3 = 0
    s21 = schur_poly((2, 1), 3)
    assert {e[:2]: c for e, c in s21.items() if e[2] == 0} == schur_poly((2, 1), 2)
    assert schur_poly((1, 1, 1), 3) == {(1, 1, 1): 1} and schur_poly((1, 1, 1), 2) == {}
    for lam in partitions(3):                                # 一般地：s_λ(x1,x2,0) = s_λ(x1,x2)
        assert {e[:2]: c for e, c in schur_poly(lam, 3).items() if e[2] == 0} == schur_poly(lam, 2)
    # Cauchy 核的三種展開（次數 3、3+3 個變數）
    kernel = cauchy_degree(3)
    for kind in "hps":
        terms = cauchy_terms(kind)
        assert poly_sum(terms) == kernel, kind
        assert tuple(t.get(TARGET, 0) for t in terms) == CONTRIB[kind]
    assert CONTRIB["s"] == tuple(f * f for f in F_LAMBDA) and sum(CONTRIB["s"]) == kernel[TARGET] == 6
    # 內積
    assert tuple(tuple(schur_inner(h_lambda(a, M), monomial_sym(b, M), M) for b in PARTS) for a in PARTS) == GRAM_HM
    assert tuple(tuple(schur_inner(p_lambda(a, M), p_lambda(b, M), M) for b in PARTS) for a in PARTS) == GRAM_PP
    assert all(GRAM_PP[i][i] == z_lambda(lam) for i, lam in enumerate(PARTS))
    assert all(schur_inner(schur_poly(a, M), schur_poly(b, M), M) == (a == b) for a in PARTS for b in PARTS)
    # ω
    for lam, lt in FLIPS:
        assert conjugate(lam) == lt and omega(schur_poly(lam, 4), 4) == schur_poly(lt, 4)
    assert omega(complete_h(3, M), M) == elementary_e(3, M)
    for mu, sg in OMEGA_SIGN.items():
        assert sg == (-1) ** (sum(mu) - len(mu)) and omega(p_lambda(mu, M), M) == poly_scale(p_lambda(mu, M), sg)
    # 特徵標
    parts, table = character_table(3)
    assert tuple(parts) == PARTS and tuple(map(tuple, table)) == CHI
    assert tuple(row[2] for row in CHI) == F_LAMBDA == tuple(len(standard_tableaux(lam)) for lam in PARTS)


# =============================================================================
# 第 1 段：讓變數無限多
# =============================================================================
def term_row(label_tex, terms, y, font_size=34):
    """VGroup(標籤, 各項, 加號)：各項分開，之後可以個別淡出。"""
    lab = Tex(label_tex, font_size=font_size)
    items, pluses = VGroup(), VGroup()
    parts = [lab]
    for k, (_, t) in enumerate(terms):
        if k:
            p = Tex("+", font_size=font_size)
            pluses.add(p)
            parts.append(p)
        mob = Tex(t, font_size=font_size)
        items.add(mob)
        parts.append(mob)
    VGroup(*parts).arrange(RIGHT, buff=0.15).move_to([0, y, 0])
    return VGroup(lab, items, pluses)


def part_infinite(scene):
    s21 = schur_poly((2, 1), 3)
    terms = poly_terms(s21)
    row3 = term_row("s_{(2,1)}(x_1,x_2,x_3)=", terms, 2.2)
    dying = [k for k, (e, _) in enumerate(terms) if e[2]]
    keep = [k for k in range(len(terms)) if k not in dying]
    dead_plus = [row3[2][k - 1] for k in dying if k > 0]
    surv = schur_poly((2, 1), 2)
    row2 = term_row("s_{(2,1)}(x_1,x_2)=", [(e, t) for e, t in poly_terms(surv)], 1.0)
    row2.align_to(row3, LEFT)
    s111 = Tex(r"s_{(1,1,1)}(x_1,x_2,x_3)=x_1x_2x_3\ \xrightarrow{\ x_3=0\ }\ 0=s_{(1,1,1)}(x_1,x_2)", font_size=32)
    s111.move_to(0.1 * DOWN).align_to(row3, LEFT)
    chain = Tex(r"\cdots\longrightarrow\Lambda_4\longrightarrow\Lambda_3\longrightarrow\Lambda_2\longrightarrow\Lambda_1",
                font_size=40).move_to(1.35 * DOWN)
    chain_lab = Tex(r"x_{m+1}\mapsto 0", font_size=26, fill_color=MUTED_COLOR).next_to(chain, UP, buff=0.12)
    moral = mixed("每個次數 ", "$n$", " 在 ", "$m\\ge n$", " 後就穩定：拼起來得到對稱函數環 ", "$\\Lambda$",
                  font_size=26, color=OK_COLOR).move_to(2.45 * DOWN)
    assert_in_frame(row3, row2, s111, chain, chain_lab, moral)
    for a, b in [(row3, row2), (row2, s111), (s111, chain_lab), (chain, moral)]:
        assert_apart(a, b, gap=0.15)
    assert len(keep) == len(surv)

    scene.say("目前都只用 3 個變數；變數個數換了，公式還對嗎？")
    scene.play(FadeIn(row3[0]), LaggedStart(*[FadeIn(t) for t in list(row3[1]) + list(row3[2])], lag_ratio=0.05),
               run_time=1.0)
    scene.wait(1.2)
    scene.say("令 ", "$x_3=0$", "：含 ", "$x_3$", " 的項全部消失")
    strikes = VGroup(*[Line(row3[1][k].get_left() + 0.05 * LEFT, row3[1][k].get_right() + 0.05 * RIGHT,
                            stroke_color=RED, stroke_width=3) for k in dying])
    scene.play(*[row3[1][k].animate.set_fill(RED) for k in dying], run_time=0.6)
    scene.play(ShowCreation(strikes), *[row3[1][k].animate.set_opacity(0.35) for k in dying],
               *[p.animate.set_opacity(0.35) for p in dead_plus], run_time=0.8)
    scene.wait(0.5)
    scene.say("剩下的正好是兩個變數的 ", "$s_{(2,1)}$")
    scene.play(FadeIn(row2[0]), *[TransformFromCopy(row3[1][k], row2[1][i]) for i, k in enumerate(keep)],
               FadeIn(row2[2]), run_time=0.9)
    scene.wait(1.1)
    scene.say("列數比變數多的 ", "$s_\\lambda$", " 則變成 0：三列的表塞不進兩個數字")
    scene.play(FadeIn(s111, shift=0.15 * RIGHT), run_time=0.8)
    scene.wait(1.6)
    scene.say("所以 ", "$x_{m+1}\\mapsto 0$", " 把 ", "$s_\\lambda$", " 送到 ", "$s_\\lambda$", " 或 0：各層彼此相容")
    scene.play(FadeIn(chain), FadeIn(chain_lab), run_time=0.8)
    scene.wait(1.3)
    scene.say("把所有層接起來，就像讓變數有無限多個")
    scene.play(FadeIn(moral, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：Cauchy 核的三種展開
# =============================================================================
def part_cauchy(scene):
    kernel = Tex(r"\prod_{i,j}\frac{1}{1-x_iy_j}", font_size=40).move_to([-4.6, 2.45, 0])
    head = VGroup(mixed("次數 3 的部分（左因子用 ", "$x$", "、右因子用 ", "$y$", "）", font_size=22, color=MUTED_COLOR),
                  mixed("黃色：", "$x_1x_2x_3\\,y_1y_2y_3$", " 的係數", font_size=22, color=YELLOW))
    head.arrange(DOWN, buff=0.12).move_to([2.1, 2.45, 0])
    specs = (("h", H_COL, r"=\sum_\lambda h_\lambda(x)\,m_\lambda(y)"),
             ("p", P_COL, r"=\sum_\lambda\frac{p_\lambda(x)\,p_\lambda(y)}{z(\lambda)}"),
             ("s", S_COL, r"=\sum_\lambda s_\lambda(x)\,s_\lambda(y)"))
    col_x = (-0.6, 2.1, 4.8)
    rows = []
    for r, (kind, col, gen_tex) in enumerate(specs):
        y = 1.25 - 1.3 * r
        dy = 0.75 if kind == "p" else 0.55
        gen = Tex(gen_tex, font_size=32, fill_color=col).move_to([-6.2, y, 0], aligned_edge=LEFT)
        terms, pluses, nums = VGroup(), VGroup(), VGroup()
        for k, lam in enumerate(PARTS):
            s = tuple_str(lam)
            if kind == "h":
                t = f"h_{{{s}}}m_{{{s}}}"
            elif kind == "p":
                t = rf"\frac{{p_{{{s}}}p_{{{s}}}}}{{{z_lambda(lam)}}}"
            else:
                t = f"s_{{{s}}}s_{{{s}}}"
            terms.add(Tex(t, font_size=30).move_to([col_x[k], y, 0]))
            nums.add(Tex(str(CONTRIB[kind][k]), font_size=28, fill_color=YELLOW).move_to([col_x[k], y - dy, 0]))
            if k:
                pluses.add(Tex("+", font_size=30).move_to([(col_x[k - 1] + col_x[k]) / 2, y, 0]))
        total = Tex(rf"\Sigma={sum(CONTRIB[kind])}", font_size=26, fill_color=YELLOW).move_to([6.25, y - dy, 0])
        rows.append(VGroup(gen, terms, pluses, nums, total))
    assert_in_frame(kernel, head, *rows)
    assert_apart(VGroup(kernel, head), VGroup(*rows), gap=0.15)
    assert_apart(kernel, head, gap=0.3)
    for row in rows:
        assert_apart(row[0], VGroup(row[1], row[2]), gap=0.2)
        assert_apart(row[1][2], row[4], gap=0.05)
        for a, b in zip(row[1], row[2]):
            assert_apart(a, b, gap=0.05)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a, b, gap=0.1)
    note = mixed("$1+4+1=1^2+2^2+1^2=3!$", font_size=24, color=OK_COLOR).move_to([3.0, -2.6, 0])
    assert_in_frame(note)
    assert_apart(rows[2], note, gap=0.1)

    scene.say("Cauchy 核：", "$x$", " 和 ", "$y$", " 兩組變數攪在一起的無窮乘積")
    scene.play(FadeIn(kernel, shift=0.1 * DOWN), run_time=0.8)
    scene.wait(1.0)
    caps = (("用 ", "$h$", " 和 ", "$m$", " 展開"), ("用冪和展開：分母又是 ", "$z(\\lambda)$"),
            ("用 Schur 多項式展開：兩邊是同一個 ", "$s_\\lambda$"))
    for row, cap in zip(rows, caps):
        scene.say(*cap)
        scene.play(FadeIn(row[0], shift=0.15 * RIGHT), run_time=0.6)
        scene.play(LaggedStart(*[FadeIn(t) for t in list(row[1]) + list(row[2])], lag_ratio=0.1), run_time=0.7)
        scene.wait(0.7)
    scene.say("在 3+3 個變數裡比對次數 3 的部分：三種寫法完全相同")
    scene.play(FadeIn(head), run_time=0.6)
    scene.wait(1.0)
    scene.say("挑一個單項式看係數：三列都加到 6")
    for row in rows:
        scene.play(LaggedStart(*[FadeIn(n, scale=1.3) for n in row[3]], lag_ratio=0.15), FadeIn(row[4]), run_time=0.7)
    scene.say("Schur 那一列的 1、4、1 是標準表個數的平方")
    scene.play(FadeIn(note, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.8)


# =============================================================================
# 第 3 段：內積
# =============================================================================
def gram_table(title_tex, A, x_center, y_top, color, cw=1.05, rh=0.6, lw=1.4):
    x0 = x_center - (lw + 3 * cw) / 2
    title = Tex(title_tex, font_size=38, fill_color=color).move_to([x_center, y_top, 0])
    heads = VGroup(*[Tex(tuple_str(mu), font_size=24, fill_color=MUTED_COLOR)
                     .move_to([x0 + lw + (j + 0.5) * cw, y_top - 0.65, 0]) for j, mu in enumerate(PARTS)])
    labs = VGroup(*[Tex(tuple_str(lam), font_size=24, fill_color=MUTED_COLOR)
                    .move_to([x0 + lw / 2, y_top - 0.65 - (i + 1) * rh, 0]) for i, lam in enumerate(PARTS)])
    nums = VGroup(*[Tex(str(A[i][j]), font_size=36, fill_color=WHITE if A[i][j] else GREY_D)
                    .move_to([x0 + lw + (j + 0.5) * cw, y_top - 0.65 - (i + 1) * rh, 0])
                    for i in range(3) for j in range(3)])
    h_line = Line([x0, y_top - 0.65 - rh / 2, 0], [x0 + lw + 3 * cw, y_top - 0.65 - rh / 2, 0],
                  stroke_color=GREY_C, stroke_width=2)
    v_line = Line([x0 + lw, y_top - 0.4, 0], [x0 + lw, y_top - 0.65 - 3.5 * rh, 0], stroke_color=GREY_C,
                  stroke_width=2)
    corner = Tex(r"\lambda\backslash\mu", font_size=22, fill_color=MUTED_COLOR).move_to([x0 + lw / 2, y_top - 0.65, 0])
    return VGroup(title, VGroup(heads, labs, h_line, v_line, corner), nums)


def part_inner(scene):
    rule = mixed("規定 ", "$\\langle s_\\lambda,s_\\mu\\rangle=\\delta_{\\lambda\\mu}$", "：Schur 函數是正交規範基底",
                 font_size=28).move_to(2.5 * UP)
    left = gram_table(r"\langle h_\lambda,m_\mu\rangle", GRAM_HM, -3.3, 1.55, H_COL)
    right = gram_table(r"\langle p_\lambda,p_\mu\rangle", GRAM_PP, 3.3, 1.55, P_COL)
    concl = VGroup(
        mixed("$h$", " 與 ", "$m$", " 互為對偶基底；", "$p$", " 兩兩正交，長度平方是 ", "$z(\\lambda)$", font_size=26),
        mixed("（命題 3：Cauchy 核的三種展開，正好說了這三件事）", font_size=22, color=MUTED_COLOR),
    ).arrange(DOWN, buff=0.2).move_to(1.9 * DOWN)
    assert_in_frame(rule, left, right, concl)
    assert_apart(rule, VGroup(left, right), gap=0.2)
    assert_apart(left, right, gap=0.5)
    assert_apart(VGroup(left, right), concl, gap=0.2)

    scene.say("在 ", "$\\Lambda$", " 上定義內積：讓 Schur 函數彼此垂直、長度 1")
    scene.play(FadeIn(rule, shift=0.1 * DOWN), run_time=0.7)
    scene.wait(1.1)
    scene.say("實際算一算 ", "$n=3$", "：", "$h$", " 和 ", "$m$", " 配對得到單位矩陣")
    scene.play(FadeIn(left[0]), FadeIn(left[1]), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(t) for t in left[2]], lag_ratio=0.06), run_time=0.8)
    scene.wait(1.0)
    scene.say("冪和自己配對：對角線恰好是 ", "$z(\\lambda)=3,2,6$")
    scene.play(FadeIn(right[0]), FadeIn(right[1]), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(t) for t in right[2]], lag_ratio=0.06), run_time=0.8)
    scene.play(*[Indicate(right[2][4 * i], color=P_COL) for i in range(3)], run_time=0.8)
    scene.say("這正是 Cauchy 核三種展開背後的意思")
    scene.play(FadeIn(concl, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.8)


# =============================================================================
# 第 4 段：對合 ω
# =============================================================================
def flip_targets(diag, lam, top_left, cs):
    out = []
    for i, row in enumerate(lam):
        for j in range(row):
            out.append((diag.cell(i, j), np.array(top_left) + (i + 0.5) * cs * RIGHT + (j + 0.5) * cs * DOWN))
    return out


def part_omega(scene):
    title = mixed("$\\omega$", "：", "$s_\\lambda\\mapsto s_{\\tilde\\lambda}$", "（把 Young 圖沿對角線翻過來）",
                  font_size=30).move_to(2.55 * UP)
    cs = 0.5
    tls = ((-5.8, 1.6, 0), (-3.1, 1.6, 0))
    labels_before = (r"s_{(3,1)}", r"h_3=s_{(3)}")
    labels_after = (r"s_{(2,1,1)}", r"e_3=s_{(1,1,1)}")
    diags, axes, labs, labs2 = [], VGroup(), VGroup(), VGroup()
    for (lam, lt), tl, a, b in zip(FLIPS, tls, labels_before, labels_after):
        assert tuple_str(lam) in a and tuple_str(lt) in b
        d = YoungDiagramMob(lam, cell_size=cs, top_left=np.array(tl, dtype=float))
        d.cells.set_fill(TEAL, opacity=0.4)
        diags.append(d)
        axes.add(DashedLine(np.array(tl) + 0.15 * UL, np.array(tl) + 1.75 * DR, stroke_color=GREY_B))
        x = tl[0] + 0.85
        labs.add(Tex(a, font_size=30).move_to([x, -0.45, 0]))
        labs2.add(Tex(b, font_size=30, fill_color=TEAL).move_to([x, -0.45, 0]))
    p_lines = VGroup(*[Tex(rf"\omega(p_{{{tuple_str(mu)}}})=" + ("" if sg > 0 else "-") + f"p_{{{tuple_str(mu)}}}",
                           font_size=32, fill_color=P_COL if sg > 0 else RED)
                       for mu, sg in OMEGA_SIGN.items()]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    p_lines.move_to([3.6, 0.75, 0])
    p_gen = Tex(r"\omega(p_\mu)=(-1)^{|\mu|-\ell(\mu)}\,p_\mu", font_size=32).next_to(p_lines, DOWN, buff=0.4)
    concl = mixed("$\\omega$", " 保持乘法與內積，做兩次就回到原狀；", "$h_\\lambda\\leftrightarrow e_\\lambda$",
                  font_size=26, color=OK_COLOR).move_to(2.5 * DOWN)
    flipped = VGroup(*[YoungDiagramMob(lt, cell_size=cs, top_left=np.array(tl, dtype=float))
                       for (_, lt), tl in zip(FLIPS, tls)])
    left_all = VGroup(*diags, flipped, axes, labs, labs2)
    assert_in_frame(title, left_all, p_lines, p_gen, concl)
    assert_apart(title, VGroup(left_all, p_lines), gap=0.2)
    assert_apart(left_all, VGroup(p_lines, p_gen), gap=0.4)
    assert_apart(VGroup(left_all, p_lines, p_gen), concl, gap=0.15)
    assert_apart(flipped[0], flipped[1], gap=0.3)
    assert_apart(labs2[0], labs2[1], gap=0.15)
    assert_apart(flipped, labs2, gap=0.1)

    scene.say("最後一個工具：對合 ", "$\\omega$", "，把每個 ", "$s_\\lambda$", " 換成轉置形狀的 ", "$s_{\\tilde\\lambda}$")
    scene.play(FadeIn(title, shift=0.1 * DOWN), run_time=0.7)
    scene.play(*[FadeIn(d) for d in diags], FadeIn(labs), run_time=0.7)
    scene.play(ShowCreation(axes), run_time=0.5)
    scene.say("沿對角線翻轉：列變成行")
    moves = []
    for d, (lam, _), tl in zip(diags, FLIPS, tls):
        moves += [c.animate(path_arc=-PI / 2).move_to(p) for c, p in flip_targets(d, lam, tl, cs)]
    scene.play(*moves, *[ReplacementTransform(a, b) for a, b in zip(labs, labs2)], run_time=1.4)
    scene.wait(1.0)
    scene.say("一列 ", "$(3)$", " 翻成一行 ", "$(1,1,1)$", "：", "$\\omega(h_3)=e_3$", "，", "$h$", " 和 ", "$e$", " 互換")
    scene.play(Indicate(labs2[1], color=TEAL), run_time=0.9)
    scene.wait(1.0)
    scene.say("冪和只差一個正負號：偶排列型不變號，奇的變號")
    scene.play(LaggedStart(*[FadeIn(t, shift=0.15 * LEFT) for t in p_lines], lag_ratio=0.3), run_time=1.1)
    scene.play(FadeIn(p_gen), run_time=0.6)
    scene.wait(1.1)
    scene.play(FadeIn(concl, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)


# =============================================================================
# 第 5 段：預告——特徵標表
# =============================================================================
def part_preview(scene):
    top = Tex(r"p_\mu=\sum_\lambda\chi^\lambda_\mu\,s_\lambda", font_size=42).move_to([-3.4, 2.35, 0])
    tag = mixed("預告第 7 章", font_size=26, color=YELLOW).move_to([2.6, 2.35, 0])
    cw, rh, x0, y0 = 1.2, 0.62, -6.0, 1.3
    heads = VGroup(*[Tex(r"\mu=" + tuple_str(mu) if j == 0 else tuple_str(mu), font_size=26, fill_color=MUTED_COLOR)
                     .move_to([x0 + 1.6 + (j + 0.5) * cw + (0.0 if j else -0.3), y0, 0]) for j, mu in enumerate(PARTS)])
    labs = VGroup(*[Tex(r"\chi^{" + tuple_str(lam) + "}", font_size=28, fill_color=MUTED_COLOR)
                    .move_to([x0 + 0.8, y0 - (i + 1) * rh, 0]) for i, lam in enumerate(PARTS)])
    nums = VGroup(*[VGroup(*[Tex(str(CHI[i][j]), font_size=34).move_to([x0 + 1.6 + (j + 0.5) * cw, y0 - (i + 1) * rh, 0])
                             for j in range(3)]) for i in range(3)])
    h_line = Line([x0, y0 - rh / 2, 0], [x0 + 1.6 + 3 * cw, y0 - rh / 2, 0], stroke_color=GREY_C, stroke_width=2)
    table = VGroup(heads, labs, nums, h_line)
    col = VGroup(*[nums[i][2] for i in range(3)])
    box = SurroundingRectangle(col, buff=0.12, color=YELLOW, stroke_width=3)
    expl = VGroup(
        mixed("$\\mu=(1,1,1)$", " 那一行：", "$1,2,1$", font_size=26),
        mixed("＝各形狀的標準表個數 ", "$f^\\lambda$", font_size=26),
        Tex(r"p_1^3=s_{(3)}+2s_{(2,1)}+s_{(1,1,1)}", font_size=32),
    ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0.6, 0.0, 0], aligned_edge=LEFT)
    final = mixed("這張表就是對稱群 ", "$S_3$", " 的特徵標表", font_size=30, color=OK_COLOR).move_to(2.2 * DOWN)
    assert_in_frame(top, tag, table, box, expl, final)
    assert_apart(VGroup(top, tag), VGroup(table, expl), gap=0.2)
    assert_apart(VGroup(table, box), expl, gap=0.3)
    assert_apart(VGroup(table, expl), final, gap=0.2)
    assert_apart(top, tag, gap=0.3)

    scene.say("把冪和寫成 Schur 函數的組合，係數記作 ", "$\\chi^\\lambda_\\mu$")
    scene.play(FadeIn(top, shift=0.1 * DOWN), FadeIn(tag), run_time=0.7)
    scene.play(FadeIn(heads), FadeIn(labs), ShowCreation(h_line), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(t) for row in nums for t in row], lag_ratio=0.06), run_time=0.9)
    scene.wait(1.0)
    scene.say("最右一行是 1、2、1：正好是標準表的個數")
    scene.play(ShowCreation(box), LaggedStart(*[FadeIn(e, shift=0.1 * LEFT) for e in expl], lag_ratio=0.3),
               run_time=1.1)
    scene.wait(1.4)
    scene.say("這些整數其實是 ", "$S_3$", " 的特徵標：第 7 章揭曉")
    scene.play(FadeIn(final, shift=0.1 * UP), run_time=0.7)
    scene.wait(2.0)


class SceneF27SymFunctions(ChuScene):
    def construct(self):
        self.show_header("對稱函數環 Λ")
        check_math()
        part_infinite(self)
        self.clear_stage()
        part_cauchy(self)
        self.clear_stage()
        part_inner(self)
        self.clear_stage()
        part_omega(self)
        self.clear_stage()
        part_preview(self)
        self.wait(1.0)
