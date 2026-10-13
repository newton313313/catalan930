"""
Scene F12 —— 內容、Kostka 數與兩種序（Fulton《Young Tableaux》§2.2，書 p.25–26）

    內容 μ：1 有 μ1 個、2 有 μ2 個……；K_λμ = 形狀 λ、內容 μ 的表的個數
        例 λ=(3,2)、μ=(2,2,1)：[[1,1,2],[2,3]]、[[1,1,3],[2,2]]，K = 2；
        數字 ≤ k 的格子是 λ^(k)，鏈 ∅ ⊂ (2) ⊂ (3,1) ⊂ (3,2) 與 ∅ ⊂ (2) ⊂ (2,2) ⊂ (3,2)，每步是水平帶
    (8) h_μ1⋯h_μℓ = Σ K_λμ s_λ，例 h2 h1 h1 = s(4) + 2 s(3,1) + s(2,2) + s(2,1,1)；(9) e 的版本用 K_{λ̃μ}
    兩種序：(2,2) ⊴ (3,1) 但不包含；(4,1,1) 字典序較大但不支配 (3,3)；(2,2,2) 與 (3,1,1,1) 不可比
    kostka_matrix(4)（字典序由小到大）下三角、對角線 1；練習 2：K_λμ ≠ 0 ⟺ μ ⊴ λ（n ≤ 6 全部驗過），
        n=6：K_(4,1,1),(3,3) = 0；→ Schur 多項式對稱；K_λμ 與 μ 的順序無關（第 4 章證）

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF12_kostka.py SceneF12Kostka
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    complete_h,
    conjugate,
    contains,
    content,
    dominates,
    elementary_e,
    is_horizontal_strip,
    kostka,
    kostka_matrix,
    lex_greater,
    partitions,
    poly_mul,
    poly_sum,
    schur_poly,
    ssyt,
    young_boxes,
)

LAM_EX, MU_EX = (3, 2), (2, 2, 1)
TABS_EX = (((1, 1, 2), (2, 3)), ((1, 1, 3), (2, 2)))
CHAINS = (((2,), (3, 1), (3, 2)), ((2,), (2, 2), (3, 2)))
MU_H = (2, 1, 1)
H_TERMS = (((4,), 1), ((3, 1), 2), ((2, 2), 1), ((2, 1, 1), 1))       # K_{λ,(2,1,1)} > 0，λ 由大到小
TABS_31 = (((1, 1, 2), (3,)), ((1, 1, 3), (2,)))
ORDER_PAIRS = (((3, 1), (2, 2)), ((4, 1, 1), (3, 3)), ((3, 1, 1, 1), (2, 2, 2)))   # (上, 下)
PARTS_4 = ((1, 1, 1, 1), (2, 1, 1), (2, 2), (3, 1), (4,))
K_4 = ((1, 0, 0, 0, 0), (3, 1, 0, 0, 0), (2, 1, 1, 0, 0), (3, 2, 1, 1, 0), (1, 1, 1, 1, 1))
ZERO_EX = ((4, 1, 1), (3, 3))
PERMS = ((2, 2, 1), (1, 2, 2), (2, 1, 2))

NUM_COLORS = {1: BLUE_C, 2: GREEN_C, 3: GOLD}
BIG, SMALL = TEAL, RED                     # 部分和：上面較大／下面較大


def chain_of(T):
    """λ^(k)＝數字 ≤ k 的格子形成的形狀，k = 1..最大的數。"""
    top = max(v for row in T for v in row)
    return tuple(tuple(c for c in (sum(v <= k for v in row) for row in T) if c) for k in range(1, top + 1))


def psums(lam, n):
    lam = tuple(lam) + (0,) * (n - len(lam))
    return tuple(sum(lam[:i + 1]) for i in range(n))


def check_math():
    assert tuple(ssyt(LAM_EX, content=MU_EX)) == TABS_EX and kostka(LAM_EX, MU_EX) == len(TABS_EX) == 2
    for T, ch in zip(TABS_EX, CHAINS):
        assert content(T) == MU_EX and chain_of(T) == ch and ch[-1] == LAM_EX
        prev = ()
        for k, lam in enumerate(ch):
            assert is_horizontal_strip(lam, prev) and sum(lam) - sum(prev) == MU_EX[k]
            prev = lam
    # (8)(9)：m = 4 個變數時把多項式乘開比較
    terms = tuple((lam, kostka(lam, MU_H)) for lam in sorted(partitions(4), reverse=True) if kostka(lam, MU_H))
    assert terms == H_TERMS and kostka((1, 1, 1, 1), MU_H) == 0
    m = 4
    hs = poly_mul(poly_mul(complete_h(2, m), complete_h(1, m)), complete_h(1, m))
    assert hs == poly_sum({e: c * k for e, c in schur_poly(lam, m).items()} for lam, k in H_TERMS)
    es = poly_mul(poly_mul(elementary_e(2, m), elementary_e(1, m)), elementary_e(1, m))
    assert es == poly_sum({e: c * kostka(conjugate(lam), MU_H) for e, c in schur_poly(lam, m).items()}
                          for lam in partitions(4))
    assert tuple(ssyt((3, 1), content=MU_H)) == TABS_31 and len(TABS_31) == dict(H_TERMS)[(3, 1)]
    # 兩種序
    (a, b), (c, d), (e, f) = ORDER_PAIRS
    assert dominates(a, b) and not contains(a, b)
    assert lex_greater(c, d) and not dominates(c, d) and not dominates(d, c)
    assert lex_greater(e, f) and not dominates(e, f) and not dominates(f, e)
    # Kostka 矩陣；練習 2 對 n ≤ 6 全部驗過
    parts, K = kostka_matrix(4)
    assert tuple(parts) == PARTS_4 and tuple(map(tuple, K)) == K_4
    for n in range(1, 7):
        parts, K = kostka_matrix(n)
        for i, lam in enumerate(parts):
            assert K[i][i] == 1 and all(K[i][j] == 0 for j in range(i + 1, len(parts)))
            assert all((K[i][j] != 0) == dominates(lam, mu) for j, mu in enumerate(parts))
    assert kostka(*ZERO_EX) == 0 and lex_greater(*ZERO_EX) and not dominates(*ZERO_EX)
    assert conjugate(ZERO_EX[0])[0] == 3 > len(ZERO_EX[1])        # 第一行 3 格，只有 2 種數字
    assert [kostka(LAM_EX, p) for p in PERMS] == [2, 2, 2]


def kname(lam, mu):
    return f"K_{{{tuple_str(lam)},{tuple_str(mu)}}}"


# =============================================================================
# 第 1 段：內容與 Kostka 數；水平帶的鏈
# =============================================================================
def part_kostka(scene):
    d1 = mixed("表的內容 ", "$\\mu=(\\mu_1,\\mu_2,\\dots)$", "：1 有 ", "$\\mu_1$", " 個、2 有 ", "$\\mu_2$",
               " 個、……", font_size=26)
    d2 = mixed("Kostka 數 ", "$K_{\\lambda\\mu}$", "＝形狀 ", "$\\lambda$", "、內容 ", "$\\mu$", " 的表的個數",
               font_size=26)
    defs = VGroup(d1, d2).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-6.3, 2.5, 0], aligned_edge=LEFT)
    cs, ccs = 0.62, 0.36
    rows = []
    for r, (T, ch) in enumerate(zip(TABS_EX, CHAINS)):
        y_top = 1.45 - 1.85 * r
        tm = tableau_mob(T, cs, top_left=(-6.2, y_top, 0))
        y_mid = y_top - ccs / 2
        empty = Tex(r"\varnothing", font_size=34).move_to([-3.75, y_mid, 0], aligned_edge=LEFT)
        x = empty.get_right()[0]
        subs, diags = VGroup(), VGroup()
        for lam in ch:
            subs.add(Tex(r"\subset", font_size=34).move_to([x + 0.32, y_mid, 0]))
            dg = YoungDiagramMob(lam, cell_size=ccs, top_left=np.array([x + 0.64, y_top, 0.0]))
            for i, j in young_boxes(lam):
                dg.cell(i, j).set_fill(NUM_COLORS[T[i][j]], opacity=0.75)
            diags.add(dg)
            x = dg.get_right()[0]
        names = VGroup(*[Tex(tuple_str(lam), font_size=22, fill_color=MUTED_COLOR)
                         .move_to([dg.get_center()[0], y_top - 2 * ccs - 0.25, 0]) for dg, lam in zip(diags, ch)])
        rows.append((T, tm, empty, subs, diags, names))
    expl = VGroup(
        mixed("數字 ", "$\\le k$", " 的格子 ", "$\\to$", " ", "$\\lambda^{(k)}$", font_size=24),
        mixed("$\\lambda^{(k)}/\\lambda^{(k-1)}$", "：", "$\\mu_k$", " 格的水平帶", font_size=24),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.2, 0.3, 0], aligned_edge=LEFT)
    result = mixed("$" + kname(LAM_EX, MU_EX) + f"={len(TABS_EX)}$", "＝表的個數＝水平帶鏈的個數", font_size=28)
    result.move_to(2.45 * DOWN)
    frame = SurroundingRectangle(result, buff=0.15, color=OK_COLOR, stroke_width=3)
    all_rows = VGroup(*[VGroup(*row[1:]) for row in rows])
    assert_in_frame(defs, all_rows, expl, frame)
    assert_apart(defs, all_rows, gap=0.2)
    assert_apart(all_rows, expl, gap=0.3)
    assert_apart(all_rows, frame, gap=0.15)
    assert_apart(VGroup(*rows[0][1:]), VGroup(*rows[1][1:]), gap=0.2)
    for _, tm, empty, subs, diags, names in rows:
        assert_apart(tm, empty, gap=0.3)
        for a, b in zip([empty] + list(diags), subs):
            assert_apart(a, b, gap=0.05)
        for a, b in zip(subs, diags):
            assert_apart(a, b, gap=0.05)

    scene.say("表的內容：每個數字各出現幾次")
    scene.play(FadeIn(d1), run_time=0.7)
    scene.wait(1.2)
    scene.say("Kostka 數 ", "$K_{\\lambda\\mu}$", "：形狀 ", "$\\lambda$", "、內容 ", "$\\mu$", " 的表有幾個")
    scene.play(FadeIn(d2), run_time=0.7)
    scene.wait(1.0)
    scene.say("例：", "$\\lambda=" + tuple_str(LAM_EX) + "$", "、", "$\\mu=" + tuple_str(MU_EX) + "$",
              f"：只有 {len(TABS_EX)} 個表")
    scene.play(*[FadeIn(row[1], shift=0.15 * RIGHT) for row in rows], run_time=0.8)
    scene.wait(1.0)
    scene.say("依序塗 1、2、3：數字 ", "$\\le k$", " 的格子總是排成一個 Young 圖 ", "$\\lambda^{(k)}$")
    scene.play(*[FadeIn(row[2]) for row in rows], run_time=0.4)
    for k in range(1, len(MU_EX) + 1):
        anims = []
        for T, tm, empty, subs, diags, names in rows:
            anims += [tm.cell(i, j).animate.set_fill(NUM_COLORS[k], opacity=0.55)
                      for i, j in young_boxes(LAM_EX) if T[i][j] == k]
            anims += [FadeIn(subs[k - 1]), FadeIn(diags[k - 1], shift=0.1 * RIGHT), FadeIn(names[k - 1])]
        scene.play(*anims, run_time=0.8)
        scene.wait(0.5)
    scene.say("每一步新加的格子兩兩不同行：都是水平帶")
    scene.play(FadeIn(expl, shift=0.15 * LEFT), run_time=0.8)
    scene.wait(1.6)
    scene.say("所以 ", "$K_{\\lambda\\mu}$", " 也是「水平帶鏈」的個數：這裡是 ", f"${len(TABS_EX)}$")
    scene.play(FadeIn(result), ShowCreation(frame), run_time=0.9)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：(8) 與 (9)
# =============================================================================
def part_h(scene):
    f8 = mixed("(8)  ", "$h_{\\mu_1}h_{\\mu_2}\\cdots h_{\\mu_\\ell}=\\sum_\\lambda K_{\\lambda\\mu}\\,s_\\lambda$",
               font_size=30).move_to(2.6 * UP)
    why = mixed("由 (6)：每乘一個 ", "$h_{\\mu_k}$", " 就加一條 ", "$\\mu_k$", " 格的水平帶，走到 ", "$\\lambda$",
                " 的走法有 ", "$K_{\\lambda\\mu}$", " 種", font_size=24, color=MUTED_COLOR).move_to(1.85 * UP)
    parts = [Tex("".join(f"h_{p}" for p in MU_H), font_size=42), Tex("=", font_size=42)]
    coef = coef_term = None
    for k, (lam, c) in enumerate(H_TERMS):
        if k:
            parts.append(Tex("+", font_size=42))
        term = VGroup(Tex(f"s_{{{tuple_str(lam)}}}", font_size=42))
        if c > 1:
            coef = Tex(str(c), font_size=42, fill_color=YELLOW)
            term = VGroup(coef, term[0]).arrange(RIGHT, buff=0.06)
            coef_term = term
        parts.append(term)
    row = VGroup(*parts).arrange(RIGHT, buff=0.18).move_to(0.75 * UP)
    tabs = VGroup(*[tableau_mob(T, 0.45) for T in TABS_31]).arrange(RIGHT, buff=0.35)
    tabs.next_to(coef_term, DOWN, buff=0.45)
    tabs_lab = mixed("內容 ", "$" + tuple_str(MU_H) + "$", " 的 ", "$(3,1)$", " 形表", font_size=20,
                     color=YELLOW).next_to(tabs, DOWN, buff=0.15)
    missing = mixed("$(1,1,1,1)$", " 不出現：", "$" + kname((1, 1, 1, 1), MU_H) + "=0$", font_size=22,
                    color=MUTED_COLOR).move_to([4.05, -0.6, 0])
    f9 = mixed("(9)  ", "$e_{\\mu_1}\\cdots e_{\\mu_\\ell}=\\sum_\\lambda K_{\\tilde\\lambda\\mu}\\,s_\\lambda$",
               font_size=30).move_to(1.85 * DOWN)
    f9_sub = mixed("$\\tilde\\lambda$", "：", "$\\lambda$", " 的轉置（乘 ", "$e_p$",
                   " 加的是垂直帶，轉置後就是水平帶）", font_size=22, color=MUTED_COLOR).move_to(2.68 * DOWN)
    assert_in_frame(f8, why, row, tabs, tabs_lab, missing, f9, f9_sub)
    for a, b in [(f8, why), (why, row), (row, tabs), (tabs_lab, f9), (f9, f9_sub), (row, missing),
                 (VGroup(tabs, tabs_lab), missing), (missing, f9)]:
        assert_apart(a, b, gap=0.12)

    scene.say("由 Pieri 公式 (6)，從 1 開始依序乘上 ", "$h_{\\mu_1},h_{\\mu_2},\\dots$")
    scene.play(FadeIn(f8), run_time=0.8)
    scene.play(FadeIn(why), run_time=0.6)
    scene.wait(1.4)
    scene.say("例：", "$\\mu=" + tuple_str(MU_H) + "$", "：", "$s_{(3,1)}$", " 的係數是 ",
              f"${dict(H_TERMS)[(3, 1)]}$", "，正是兩個表")
    scene.play(FadeIn(row), run_time=0.9)
    scene.play(Indicate(coef, color=YELLOW), FadeIn(tabs, shift=0.15 * UP), FadeIn(tabs_lab), run_time=1.0)
    scene.play(FadeIn(missing), run_time=0.6)
    scene.wait(1.6)
    scene.say("(9) 同理：乘 ", "$e_p$", " 加垂直帶，所以係數換成轉置形狀的 Kostka 數")
    scene.play(FadeIn(f9), FadeIn(f9_sub), run_time=0.8)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：字典序與支配序
# =============================================================================
def order_panel(top, bottom, x):
    """兩個分割的部分和表（上面較大＝青、下面較大＝紅）。"""
    n = max(len(top), len(bottom))
    st, sb = psums(top, n), psums(bottom, n)
    title = mixed("前 ", "$i$", " 項的和", font_size=20, color=MUTED_COLOR)
    grid = VGroup()
    for lam, sums in ((top, st), (bottom, sb)):
        line = VGroup(Tex(tuple_str(lam), font_size=24))
        for v, a, b in zip(sums, st, sb):                # 同一欄的兩個數用同一種顏色
            col = BIG if a > b else (SMALL if a < b else WHITE)
            line.add(Tex(str(v), font_size=28, fill_color=col))
        grid.add(line)
    for line in grid:
        line[0].move_to([x - 0.95, 0, 0], aligned_edge=RIGHT)
        for k, t in enumerate(line[1:]):
            t.move_to([x - 0.6 + 0.48 * k, 0, 0], aligned_edge=LEFT)
    grid[0].shift(0.45 * UP)
    grid[1].shift(0.15 * DOWN)
    title.move_to([x, 1.15, 0])
    return VGroup(title, grid), st, sb


def part_orders(scene):
    lex = mixed("字典序：從第一項比起，第一個不同的地方較大者為大（全序）", font_size=24)
    dom = mixed("支配序 ", "$\\mu\\trianglelefteq\\lambda$", "：每個 ", "$i$", " 都有 ",
                "$\\mu_1+\\cdots+\\mu_i\\le\\lambda_1+\\cdots+\\lambda_i$", font_size=24)
    VGroup(lex, dom).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-6.3, 2.5, 0], aligned_edge=LEFT)
    xs = (-4.4, 0.1, 4.6)
    panels = []
    for (top, bottom), x in zip(ORDER_PAIRS, xs):
        panels.append(order_panel(top, bottom, x))
    (a, b), (c, d), (e, f) = [tuple(tuple_str(p) for p in pair) for pair in ORDER_PAIRS]
    _, st1, sb1 = panels[1]
    bad = next(i for i in range(len(st1)) if st1[i] < sb1[i]) + 1
    verdicts = [
        VGroup(Tex(b + r"\trianglelefteq " + a, font_size=30, fill_color=OK_COLOR),
               mixed("但 ", "$" + b + r"\not\subset " + a + "$", font_size=22)),
        VGroup(mixed("字典序 ", "$" + c + ">" + d + "$", font_size=22),
               mixed("但 ", "$" + c + "$", " 不支配 ", "$" + d + "$", font_size=22)),
        VGroup(mixed("互不支配：不可比", font_size=22),
               mixed("（字典序仍有 ", "$" + e + ">" + f + "$", "）", font_size=20, color=MUTED_COLOR)),
    ]
    for v, x in zip(verdicts, xs):
        v.arrange(DOWN, buff=0.18).move_to([x, -0.95, 0])
    # (2,2) 放不進 (3,1)：多出來的那一格畫紅色
    big, small = ORDER_PAIRS[0]
    pic = YoungDiagramMob(big, cell_size=0.4)
    pic.fill_cells([bx for bx in young_boxes(small) if bx in young_boxes(big)], BLUE_C, opacity=0.6)
    extra = VGroup(*[Square(side_length=0.4, stroke_color=RED, stroke_width=3).set_fill(RED, opacity=0.5)
                     .move_to(pic.cell(0, 0).get_center() + 0.4 * (j * RIGHT + i * DOWN))
                     for i, j in young_boxes(small) if (i, j) not in young_boxes(big)])
    VGroup(pic, extra).next_to(verdicts[0], DOWN, buff=0.3)
    legend = mixed("青：上面的和較大　紅：下面的和較大", font_size=20, color=MUTED_COLOR).move_to([4.4, -2.55, 0])
    assert_in_frame(lex, dom, *[p[0] for p in panels], *verdicts, pic, extra, legend)
    for k in range(3):
        assert_apart(panels[k][0], verdicts[k], gap=0.15)
        assert_apart(VGroup(lex, dom), panels[k][0], gap=0.2)
        if k:
            assert_apart(VGroup(panels[k - 1][0], verdicts[k - 1]), VGroup(panels[k][0], verdicts[k]), gap=0.3)
    assert_apart(VGroup(pic, extra), legend, gap=0.3)
    assert_apart(verdicts[2], legend, gap=0.15)

    scene.say("分割之間有兩種序：字典序是全序，支配序比較部分和")
    scene.play(FadeIn(lex), run_time=0.6)
    scene.play(FadeIn(dom), run_time=0.6)
    scene.wait(1.6)
    caps = [
        ("$" + b + r"\trianglelefteq " + a + "$", "，可是 ", "$" + b + "$", " 的圖放不進 ", "$" + a + "$"),
        ("$" + c + "$", f" 的字典序較大，但第 {bad} 個部分和較小：不支配"),
        ("$" + e + "$", " 與 ", "$" + f + "$", "：部分和一下大、一下小，互不支配"),
    ]
    for k, (panel, st, sb) in enumerate(panels):
        scene.say(*caps[k])
        anims = [FadeIn(panel, shift=0.1 * DOWN), FadeIn(verdicts[k])]
        if k == 0:
            anims += [FadeIn(pic), FadeIn(extra)]
        if k == 1:
            anims.append(FadeIn(legend))
        scene.play(*anims, run_time=0.9)
        scene.wait(2.4)


# =============================================================================
# 第 4 段：Kostka 矩陣（下三角）、練習 2 與推論
# =============================================================================
def kostka_table(parts, K, x0, y0, cw=1.12, rh=0.5, lw=1.5):
    n = len(parts)
    corner = Tex(r"\lambda\backslash\mu", font_size=24, fill_color=MUTED_COLOR).move_to([x0 + lw / 2, y0 - rh / 2, 0])
    heads = VGroup(*[Tex(tuple_str(mu), font_size=22, fill_color=MUTED_COLOR)
                     .move_to([x0 + lw + (j + 0.5) * cw, y0 - rh / 2, 0]) for j, mu in enumerate(parts)])
    rows = VGroup(*[Tex(tuple_str(lam), font_size=22, fill_color=MUTED_COLOR)
                    .move_to([x0 + lw / 2, y0 - (i + 1.5) * rh, 0]) for i, lam in enumerate(parts)])
    diag, upper, lower = VGroup(), VGroup(), VGroup()
    for i in range(n):
        for j in range(n):
            t = Tex(str(K[i][j]), font_size=30).move_to([x0 + lw + (j + 0.5) * cw, y0 - (i + 1.5) * rh, 0])
            (diag if i == j else upper if j > i else lower).add(t)
    h_line = Line([x0, y0 - rh, 0], [x0 + lw + n * cw, y0 - rh, 0], stroke_color=GREY_C, stroke_width=2)
    v_line = Line([x0 + lw, y0, 0], [x0 + lw, y0 - (n + 1) * rh, 0], stroke_color=GREY_C, stroke_width=2)
    return VGroup(corner, heads, rows, h_line, v_line), diag, upper, lower


def part_matrix(scene):
    parts, K = kostka_matrix(4)
    frame_, diag, upper, lower = kostka_table(parts, K, -6.6, 2.75)
    title = mixed("$n=4$", "，字典序由小到大", font_size=24).next_to(frame_, DOWN, buff=0.2)
    l1 = mixed("下三角，對角線全是 1", font_size=26)
    l2 = mixed("練習 2：", "$K_{\\lambda\\mu}\\neq 0\\iff\\mu\\trianglelefteq\\lambda$", font_size=26)
    l3 = mixed("$n=6$", "：", "$" + tuple_str(ZERO_EX[0]) + ">" + tuple_str(ZERO_EX[1]) + "$", "（字典序），但",
               font_size=24)
    l4 = mixed("$" + kname(*ZERO_EX) + f"={kostka(*ZERO_EX)}$", font_size=26)
    right = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    right.move_to([1.3, 2.75, 0], aligned_edge=UL)
    pic = YoungDiagramMob(ZERO_EX[0], cell_size=0.42)
    col_len, kinds = conjugate(ZERO_EX[0])[0], len(ZERO_EX[1])
    why = VGroup(zh(f"第一行要 {col_len} 個不同的數，", font_size=20, color=MUTED_COLOR),
                 zh("但只有 " + "、".join(str(k) for k in range(1, kinds + 1)) + " 可用", font_size=20,
                    color=MUTED_COLOR)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    VGroup(pic, why).arrange(RIGHT, buff=0.3).next_to(right, DOWN, buff=0.3, aligned_edge=LEFT)
    labels = [str(k) for k in range(1, kinds + 1)] + ["?"] * (col_len - kinds)
    marks = VGroup(*[Tex(s, font_size=26, fill_color=RED if s == "?" else WHITE).move_to(pic.cell(i, 0))
                     for i, s in enumerate(labels)])
    c1 = mixed("下三角 ", "$\\Rightarrow$", " (8) 可以反解：", "$s_\\lambda$", " 寫成 ", "$h_\\mu$",
               " 的組合 ", "$\\Rightarrow$", " Schur 多項式是對稱多項式", font_size=24)
    perm_tex = "=".join(kname(LAM_EX, p) for p in PERMS) + f"={kostka(LAM_EX, PERMS[0])}"
    c2 = mixed("$K_{\\lambda\\mu}$", " 與 ", "$\\mu$", " 的順序無關（第 4 章證）：", "$" + perm_tex + "$",
               font_size=22)
    cons = VGroup(c1, c2).arrange(DOWN, buff=0.3).move_to(2.15 * DOWN)
    assert_in_frame(frame_, title, right, pic, why, cons)
    assert_apart(VGroup(frame_, title), right, gap=0.3)
    assert_apart(VGroup(frame_, title), VGroup(pic, why), gap=0.3)
    assert_apart(VGroup(frame_, title, pic, why, right), cons, gap=0.15)

    scene.say("把 ", "$n=4$", " 的分割依字典序由小到大排，", "$K_{\\lambda\\mu}$", " 排成一個矩陣")
    scene.play(FadeIn(frame_), FadeIn(title), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(t) for t in list(lower) + list(diag) + list(upper)], lag_ratio=0.04),
               run_time=1.2)
    scene.wait(0.6)
    scene.say("對角線都是 1，右上方全是 0：下三角矩陣")
    scene.play(diag.animate.set_fill(YELLOW), upper.animate.set_fill(GREY_D), FadeIn(l1), run_time=0.8)
    scene.wait(1.4)
    scene.say("更精確（練習 2）：", "$K_{\\lambda\\mu}\\neq 0$", " 恰好在 ", "$\\lambda$", " 支配 ", "$\\mu$", " 的時候")
    scene.play(FadeIn(l2), run_time=0.7)
    scene.wait(1.8)
    scene.say("字典序較大還不夠：", "$n=6$", " 時 ", "$" + kname(*ZERO_EX) + "=0$")
    scene.play(FadeIn(l3), FadeIn(l4), run_time=0.7)
    scene.play(FadeIn(pic), FadeIn(marks), FadeIn(why), run_time=0.8)
    scene.wait(1.8)
    scene.say("矩陣可逆，所以 ", "$s_\\lambda$", " 能用 ", "$h$", " 表示：Schur 多項式是對稱的")
    scene.play(FadeIn(c1, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.6)
    scene.say("也推得 ", "$K_{\\lambda\\mu}$", " 與 ", "$\\mu$", " 各項的順序無關（第 4 章直接證明）")
    scene.play(FadeIn(c2, shift=0.15 * UP), run_time=0.8)
    scene.wait(2.4)


class SceneF12Kostka(ChuScene):
    def construct(self):
        self.show_header("內容、Kostka 數與兩種序")
        check_math()
        part_kostka(self)
        self.clear_stage()
        part_h(self)
        self.clear_stage()
        part_orders(self)
        self.clear_stage()
        part_matrix(self)
        self.wait(1.0)
