"""
Scene F03 —— Schur 多項式（Fulton《Young Tableaux》Notation，書 p.3–4）

    每個表 T 給一個單項式 x^T：數字 i 出現 c_i 次 -> 因子 x_i^{c_i}
        書 p.2 的表 -> x^T = x1 x2^3 x3^3 x4^2 x5^4 x6^3
    s_λ(x1..xm) = Σ_T x^T（T 跑遍形狀 λ、數字取自 1..m 的表）
    例：s_(2,1)(x1,x2,x3) 的 8 個表，合併後 x1x2x3 的係數 2 = (2,1) 的標準表個數
    對調 x1、x2：各項互換位置，式子不變（對稱；一般情形書中之後才證明）
    一列：s_(n) = h_n；一行：s_(1^n) = e_n

所有數字都由 utils/tableaux.py 算出並 assert。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF03_schur.py SceneF03Schur
"""
import sys
from collections import Counter
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    FULTON_TABLEAU,
    complete_h,
    content,
    elementary_e,
    is_standard,
    is_tableau,
    kostka,
    partitions,
    schur_poly,
    shape,
    ssyt,
    standard_tableaux,
)

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2

LAM = (2, 1)               # 例子的形狀
M = 3                      # 變數個數 x1, x2, x3
NUM_COLORS = {1: BLUE_C, 2: TEAL_C, 3: GREEN_C, 4: YELLOW_D, 5: ORANGE, 6: PINK}
VAR_COLORS = {1: TEAL, 2: PINK}        # 對稱段：x1 青、x2 粉紅


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


# =============================================================================
# 多項式 -> 一個 Tex，記下每一項／每個因子是第幾個字形（上色、搬動用）
# =============================================================================
def poly_parts(terms):
    """
    terms = [(係數, 指數 tuple), ...]  ->  (tex 字串, 字形數, 每項的 slice, 每項 {變數: slice}, 加號 slice, 係數 slice)
    字形數：x_{i}^{e} = 1 + len(str(i)) + (len(str(e)) if e > 1)；係數、加號各自的位數。
    """
    s, idx = "", 0
    term_sl, fac_sl, plus_sl, coef_sl = [], [], [], []
    for k, (c, e) in enumerate(terms):
        if k > 0:
            s += "+"
            plus_sl.append(slice(idx, idx + 1))
            idx += 1
        start = idx
        if c != 1:
            s += str(c)
            coef_sl.append(slice(idx, idx + len(str(c))))
            idx += len(str(c))
        else:
            coef_sl.append(None)
        fs = {}
        for v, a in enumerate(e, start=1):
            if a == 0:
                continue
            s += f"x_{{{v}}}" + (f"^{{{a}}}" if a > 1 else "")
            g = 1 + len(str(v)) + (len(str(a)) if a > 1 else 0)
            fs[v] = slice(idx, idx + g)
            idx += g
        term_sl.append(slice(start, idx))
        fac_sl.append(fs)
    return s, idx, term_sl, fac_sl, plus_sl, coef_sl


def _shift(sl, p):
    return None if sl is None else slice(sl.start + p, sl.stop + p)


def poly_expr(terms, prefix="", suffix="", font_size=36):
    """回傳 (Tex, info)；info 的 slice 都已經加上 prefix 的字形數，可直接 tex[slice]。"""
    s, n, term_sl, fac_sl, plus_sl, coef_sl = poly_parts(terms)
    p = len(Tex(prefix)) if prefix else 0
    q = len(Tex(suffix)) if suffix else 0
    tex = Tex(prefix + s + suffix, font_size=font_size)
    assert len(tex) == p + n + q, (prefix + s + suffix, len(tex), p, n, q)
    info = {
        "prefix": slice(0, p),
        "eq": slice(p - 1, p) if p else None,
        "terms": [_shift(sl, p) for sl in term_sl],
        "factors": [{v: _shift(sl, p) for v, sl in fs.items()} for fs in fac_sl],
        "plus": [_shift(sl, p) for sl in plus_sl],
        "coef": [_shift(sl, p) for sl in coef_sl],
        "suffix": slice(p + n, p + n + q),
    }
    return tex, info


def mono_str(e):
    return poly_parts([(1, e)])[0]


def color_vars(tex, info, colors):
    for fs in info["factors"]:
        for v, sl in fs.items():
            if v in colors:
                tex[sl].set_fill(colors[v])


def tuple_str(t):
    return "(" + ",".join(str(a) for a in t) + ")"


# =============================================================================
def check_math():
    T = FULTON_TABLEAU
    assert is_tableau(T) and shape(T) == (6, 4, 4, 2)
    c = content(T)
    assert c == (1, 3, 3, 2, 4, 3)                      # 書 p.3：x1 x2^3 x3^3 x4^2 x5^4 x6^3
    assert mono_str(c) == "x_{1}x_{2}^{3}x_{3}^{3}x_{4}^{2}x_{5}^{4}x_{6}^{3}"

    tabs = ssyt(LAM, M)
    assert len(tabs) == 8 and all(is_tableau(t) and shape(t) == LAM for t in tabs)
    monos = [content(t, M) for t in tabs]
    S = schur_poly(LAM, M)
    assert S == dict(Counter(monos)) and sum(S.values()) == 8
    # 合併後的項：依「第一次出現」的順序 = 指數由大到小（字典序），x1x2x3 的係數 2
    order = list(dict.fromkeys(monos))
    assert order == sorted(S, reverse=True)
    terms = [(S[e], e) for e in order]
    assert [cf for cf, _ in terms] == [1, 1, 1, 2, 1, 1, 1]
    assert S[(1, 1, 1)] == 2 == kostka(LAM, (1, 1, 1)) == len(standard_tableaux(LAM))
    std_idx = [k for k, t in enumerate(tabs) if is_standard(t)]
    assert std_idx == [k for k, e in enumerate(monos) if e == (1, 1, 1)] == [3, 4]
    assert set(tabs[k] for k in std_idx) == set(standard_tableaux(LAM))

    # 對調 x1、x2：每一項換成指數 (b, a, c) 的項，perm[k] = 換完之後是原式的第幾項
    swapped = [(cf, (e[1], e[0]) + e[2:]) for cf, e in terms]
    perm = [order.index(e) for _, e in swapped]
    assert sorted(perm) == list(range(len(terms))) and perm == [2, 5, 0, 3, 6, 1, 4]
    assert all(S[e] == cf for cf, e in swapped)
    # 對稱：s_λ 對任何變數的排列都不變（λ ⊢ n ≤ 4、m ≤ 4，暴力檢查）
    for n in range(1, 5):
        for m in range(1, 5):
            for lam in partitions(n, max_parts=m):
                P = schur_poly(lam, m)
                for s in permutations(range(m)):
                    assert {tuple(e[s[i]] for i in range(m)): v for e, v in P.items()} == P
    # 一列 = h_n、一行 = e_n
    for n in range(1, 5):
        for m in range(1, 5):
            assert schur_poly((n,), m) == complete_h(n, m)
            assert schur_poly((1,) * n, m) == (elementary_e(n, m) if n <= m else {})
    row_tabs = ssyt((2,), M)
    col_tabs = ssyt((1, 1), M)
    assert len(row_tabs) == 6 == len(complete_h(2, M)) and len(col_tabs) == 3 == len(elementary_e(2, M))
    assert [content(t, M) for t in row_tabs] == sorted(complete_h(2, M), reverse=True)
    assert [content(t, M) for t in col_tabs] == sorted(elementary_e(2, M), reverse=True)
    return T, tabs, monos, terms, swapped, perm, std_idx, row_tabs, col_tabs


# =============================================================================
def part_monomial(scene, T):
    lam, c = shape(T), content(T)
    diag = YoungDiagramMob(lam, cell_size=0.62, top_left=np.array([-6.3, 2.6, 0.0]), entries=T, font_size=32)
    lam_lab = Tex(r"\lambda=" + tuple_str(lam), font_size=34)
    lam_lab.next_to(diag, DOWN, buff=0.3).align_to(diag, LEFT)

    xt, info = poly_expr([(1, c)], prefix="x^T=", font_size=52)
    xt.move_to(np.array([2.3, 1.95, 0.0]))
    for v, sl in info["factors"][0].items():
        xt[sl].set_fill(NUM_COLORS[v])
    general = mixed("$x^T=x_1^{c_1}x_2^{c_2}\\cdots x_m^{c_m}$", "，其中 ", "$c_i$", " 是數字 ", "$i$", " 在 ", "$T$",
                    " 裡出現的次數", font_size=26)
    general.move_to(np.array([2.3, 0.75, 0.0]))

    defn = Tex(r"s_\lambda(x_1,\dots,x_m)=\sum_{T} x^T", font_size=50)
    defn_note = mixed("$T$", " 跑遍形狀為 ", "$\\lambda$", "、數字取自 ", "$1,2,\\dots,m$", " 的所有表", font_size=26)
    defn_block = VGroup(defn, defn_note).arrange(DOWN, buff=0.3)
    defn_box = SurroundingRectangle(defn_block, buff=0.25, color=YELLOW, stroke_width=3)
    VGroup(defn_block, defn_box).move_to(np.array([0.0, -1.75, 0.0]))
    assert_in_frame(diag, lam_lab, xt, general, defn_box)
    assert_apart(diag, xt)
    assert_apart(diag, general)
    assert_apart(xt, general)
    assert_apart(lam_lab, defn_box)
    assert_apart(general, defn_box)

    scene.say("把表裡的數字當成變數的下標：每個表 ", "$T$", " 都給出一個單項式 ", "$x^T$")
    scene.play(ShowCreation(diag.cells), run_time=0.8)
    scene.play(FadeIn(diag.entries), FadeIn(lam_lab), run_time=0.6)
    scene.play(FadeIn(xt[info["prefix"]]), run_time=0.4)
    scene.say("數字 ", "$i$", " 出現幾次，", "$x_i$", " 就取幾次方")
    for v in range(1, len(c) + 1):
        cells = [(i, j) for i, row in enumerate(T) for j, a in enumerate(row) if a == v]
        assert len(cells) == c[v - 1]
        scene.play(*[diag.cell(i, j).animate.set_fill(NUM_COLORS[v], opacity=0.5) for i, j in cells],
                   FadeIn(xt[info["factors"][0][v]], shift=0.15 * UP), run_time=0.6)
        scene.wait(0.15)
    scene.say("一般寫法：", "$c_i$", " 是數字 ", "$i$", " 的個數")
    scene.play(FadeIn(general, shift=0.15 * UP), run_time=0.7)
    scene.wait(0.8)
    scene.say("Schur 多項式：把形狀 ", "$\\lambda$", " 上所有表的單項式加起來（數字只用 ", "$1$", " 到 ", "$m$", "）")
    scene.play(Write(defn), ShowCreation(defn_box), run_time=1.3)
    scene.play(FadeIn(defn_note, shift=0.15 * UP), run_time=0.6)
    scene.wait(2.0)


def part_example(scene, tabs, monos, terms, std_idx):
    n_tabs = len(tabs)
    title = mixed("例：", "$\\lambda=(2,1)$", "，", f"$m={M}$", "，數字取自 ", "$\\{1,2,3\\}$", " 的表一共 ",
                  f"${n_tabs}$", " 個", font_size=28)
    title.move_to(np.array([0.0, 2.7, 0.0]))
    diags = VGroup(*[YoungDiagramMob(LAM, cell_size=0.55, entries=t, font_size=30) for t in tabs])
    diags.arrange(RIGHT, buff=0.5).move_to(np.array([0.0, 1.5, 0.0]))
    mono_mobs = VGroup()
    for d, e in zip(diags, monos):
        m = poly_expr([(1, e)], font_size=34)[0]
        m.move_to(np.array([d.get_center()[0], 0.45, 0.0]))
        mono_mobs.add(m)

    total, info = poly_expr(terms, prefix="s_{(2,1)}(x_1,x_2,x_3)=", font_size=40)
    total.move_to(np.array([0.0, -0.75, 0.0]))
    coef_k = [k for k, (cf, _) in enumerate(terms) if cf != 1]
    assert coef_k == [3]
    coef = total[info["coef"][3]]
    term3 = total[info["terms"][3]]
    note = mixed("係數 ", "$2$", "$=$", "$1,2,3$", " 各用一次的表（標準表）的個數", font_size=26)
    note[1].set_fill(YELLOW)
    note.move_to(np.array([0.0, -1.95, 0.0]))
    assert_in_frame(title, diags, mono_mobs, total, note)
    assert_apart(title, diags)
    assert_apart(diags, mono_mobs)
    assert_apart(mono_mobs, total, gap=0.3)
    assert_apart(total, note, gap=0.3)
    for a, b in zip(mono_mobs[:-1], mono_mobs[1:]):
        assert_apart(a, b, gap=0.2)

    scene.say("具體算一個：", "$\\lambda=(2,1)$", "、只用 1、2、3，這樣的表一共 8 個")
    scene.play(FadeIn(title), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(d, shift=0.15 * DOWN) for d in diags], lag_ratio=0.12), run_time=1.6)
    scene.say("每個表寫下它的單項式")
    scene.play(LaggedStart(*[FadeIn(m, shift=0.15 * DOWN) for m in mono_mobs], lag_ratio=0.12), run_time=1.5)
    scene.wait(0.5)

    scene.say("全部加起來，相同的項合併：", "$x_1x_2x_3$", " 出現了兩次")
    order = [e for _, e in terms]
    where = [order.index(e) for e in monos]
    assert [terms[w][1] for w in where] == monos
    scene.play(FadeIn(total[info["prefix"]]), run_time=0.5)
    scene.play(*[TransformFromCopy(mono_mobs[k], total[info["terms"][where[k]]]) for k in range(n_tabs)],
               *[FadeIn(total[sl]) for sl in info["plus"]], run_time=1.6)
    scene.add(total)
    rects = VGroup(*[SurroundingRectangle(VGroup(diags[k], mono_mobs[k]), buff=0.12, color=YELLOW, stroke_width=3)
                     for k in std_idx])
    term_rect = SurroundingRectangle(term3, buff=0.1, color=YELLOW, stroke_width=3)
    scene.wait(0.4)
    scene.say("係數 2 來自這兩個表：1、2、3 各用一次，正是 ", "$(2,1)$", " 的標準表")
    scene.play(ShowCreation(rects), ShowCreation(term_rect), coef.animate.set_fill(YELLOW), run_time=0.9)
    scene.play(FadeIn(note, shift=0.15 * UP), run_time=0.6)
    scene.wait(2.0)
    return title, diags, mono_mobs, total, info, VGroup(rects, term_rect, note)


def part_symmetry(scene, terms, swapped, perm, title, diags, mono_mobs, total, info, extras):
    scene.say("把 ", "$x_1$", " 和 ", "$x_2$", " 對調，看看會發生什麼事")
    scene.play(FadeOut(title), FadeOut(diags), FadeOut(mono_mobs), FadeOut(extras),
               total.animate.move_to(np.array([0.0, 2.2, 0.0])), run_time=0.9)
    anims = []
    for fs in info["factors"]:
        for v, sl in fs.items():
            anims.append(total[sl].animate.set_fill(VAR_COLORS.get(v, WHITE)))
    scene.play(*anims, total[info["coef"][3]].animate.set_fill(WHITE), run_time=0.6)

    row2, info2 = poly_expr(swapped, prefix="s_{(2,1)}(x_2,x_1,x_3)=", font_size=40)
    color_vars(row2, info2, VAR_COLORS)
    eq1 = total[info["eq"]].get_center()
    row2.shift(np.array([eq1[0], 0.6, 0.0]) - row2[info2["eq"]].get_center())
    swap_lab = mixed("$x_1\\leftrightarrow x_2$", font_size=28, color=YELLOW)
    swap_lab.move_to(np.array([0.0, 1.4, 0.0]))
    target, info3 = poly_expr(terms, prefix="s_{(2,1)}(x_2,x_1,x_3)=", font_size=40)
    color_vars(target, info3, VAR_COLORS)
    target.shift(row2[info2["prefix"]].get_center() - target[info3["prefix"]].get_center())

    same = mixed("$s_{(2,1)}(x_2,x_1,x_3)=s_{(2,1)}(x_1,x_2,x_3)$", font_size=34, color=OK_COLOR)
    same.move_to(np.array([0.0, -0.75, 0.0]))
    sym = mixed("一般的 ", "$s_\\lambda$", " 也一樣：任意交換變數都不變，叫做「對稱多項式」", font_size=27)
    later = zh("（從定義看不出來；書中之後才證明）", font_size=22, color=MUTED_COLOR)
    VGroup(sym, later).arrange(DOWN, buff=0.22).move_to(np.array([0.0, -2.1, 0.0]))
    assert_in_frame(total, row2, target, swap_lab, same, sym, later)
    assert_apart(total, swap_lab)
    assert_apart(swap_lab, row2)
    assert_apart(row2, same, gap=0.4)
    assert_apart(same, sym)

    scene.play(FadeIn(swap_lab, scale=1.2), run_time=0.5)
    scene.play(TransformFromCopy(total[info["prefix"]], row2[info2["prefix"]]),
               *[TransformFromCopy(total[info["terms"][k]], row2[info2["terms"][k]]) for k in range(len(terms))],
               *[TransformFromCopy(total[a], row2[b]) for a, b in zip(info["plus"], info2["plus"])], run_time=1.5)
    scene.add(row2)
    scene.wait(0.6)
    scene.say("每一項都變成另一項；重新排好順序……")
    scene.play(*[Transform(row2[info2["terms"][k]], target[info3["terms"][perm[k]]], path_arc=PI / 2)
                 for k in range(len(terms))],
               *[Transform(row2[a], target[b]) for a, b in zip(info2["plus"], info3["plus"])], run_time=1.8)
    scene.wait(0.4)
    scene.say("……又回到原來的式子：對調 ", "$x_1$", "、", "$x_2$", " 不改變 ", "$s_{(2,1)}$")
    scene.play(FadeIn(same, shift=0.15 * UP), run_time=0.7)
    scene.wait(0.8)
    scene.say("一般的 Schur 多項式也對所有變數對稱，但這要等到書的後面才證明")
    scene.play(FadeIn(sym, shift=0.15 * UP), FadeIn(later), run_time=0.8)
    scene.wait(2.2)


def part_h_e(scene, row_tabs, col_tabs):
    cs = 0.4
    # ---------------------------------------------------- 一列：s_(n) = h_n
    t1 = mixed("$\\lambda=(n)$", " 只有一列：由左到右不減，數字可以重複", font_size=27)
    t1.move_to(np.array([0.0, 2.75, 0.0])).to_edge(LEFT, buff=0.6)
    g1 = Tex(r"s_{(n)}=h_n", font_size=40)
    row_terms = [(1, content(t, M)) for t in row_tabs]
    f1, i1 = poly_expr(row_terms, prefix="s_{(2)}(x_1,x_2,x_3)=", suffix="=h_2(x_1,x_2,x_3)", font_size=38)
    f1.move_to(np.array([0.0, 1.05, 0.0]))
    d1 = VGroup()
    for k, t in enumerate(row_tabs):
        d = YoungDiagramMob((2,), cell_size=cs, entries=t, font_size=26)
        d.move_to(np.array([f1[i1["terms"][k]].get_center()[0], 1.85, 0.0]))
        d1.add(d)
    # ---------------------------------------------------- 一行：s_(1^n) = e_n
    t2 = mixed("$\\lambda=(1^n)$", " 只有一行：由上到下嚴格遞增，數字不能重複", font_size=27)
    t2.move_to(np.array([0.0, 0.15, 0.0])).to_edge(LEFT, buff=0.6)
    g2 = Tex(r"s_{(1^n)}=e_n", font_size=40)
    col_terms = [(1, content(t, M)) for t in col_tabs]
    f2, i2 = poly_expr(col_terms, prefix="s_{(1,1)}(x_1,x_2,x_3)=", suffix="=e_2(x_1,x_2,x_3)", font_size=38)
    f2.move_to(np.array([0.0, -1.85, 0.0]))
    d2 = VGroup()
    for k, t in enumerate(col_tabs):
        d = YoungDiagramMob((1, 1), cell_size=cs, entries=t, font_size=26)
        d.move_to(np.array([f2[i2["terms"][k]].get_center()[0], -0.85, 0.0]))
        d2.add(d)
    g1.move_to(np.array([4.9, t1.get_center()[1], 0.0]))
    g2.move_to(np.array([4.9, t2.get_center()[1], 0.0]))
    b1 = SurroundingRectangle(g1, buff=0.15, color=YELLOW, stroke_width=3)
    b2 = SurroundingRectangle(g2, buff=0.15, color=YELLOW, stroke_width=3)
    foot = mixed("$h_n$", "：所有 ", "$n$", " 次單項式之和；", "$e_n$", "：", "$n$", " 個不同變數的乘積之和",
                 font_size=24, color=MUTED_COLOR)
    foot.move_to(np.array([0.0, -2.7, 0.0]))
    assert_in_frame(t1, g1, b1, f1, d1, t2, g2, b2, f2, d2, foot)
    assert_apart(t1, b1)
    assert_apart(t2, b2)
    assert_apart(VGroup(t1, b1), d1)
    assert_apart(d1, f1)
    assert_apart(f1, VGroup(t2, b2), gap=0.3)
    assert_apart(VGroup(t2, b2), d2)
    assert_apart(d2, f2)
    assert_apart(f2, foot)
    for grp in (d1, d2):
        for a, b in zip(grp[:-1], grp[1:]):
            assert_apart(a, b, gap=0.2)

    scene.say("只有一列的形狀：數字不減、可以重複，每個 ", "$n$", " 次單項式剛好出現一次")
    scene.play(FadeIn(t1), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(d, shift=0.1 * DOWN) for d in d1], lag_ratio=0.12), run_time=1.2)
    scene.play(FadeIn(f1[i1["prefix"]]),
               *[TransformFromCopy(d1[k].entries, f1[i1["terms"][k]]) for k in range(len(row_tabs))],
               *[FadeIn(f1[sl]) for sl in i1["plus"]], run_time=1.3)
    scene.play(FadeIn(f1[i1["suffix"]]), run_time=0.5)
    scene.add(f1)
    scene.say("所以 ", "$s_{(n)}=h_n$", "：", "$n$", " 次的完全齊次對稱多項式")
    scene.play(FadeIn(g1), ShowCreation(b1), run_time=0.7)
    scene.wait(1.0)

    scene.say("只有一行的形狀：數字嚴格遞增，等於挑 ", "$n$", " 個不同的變數相乘")
    scene.play(FadeIn(t2), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(d, shift=0.1 * DOWN) for d in d2], lag_ratio=0.15), run_time=1.0)
    scene.play(FadeIn(f2[i2["prefix"]]),
               *[TransformFromCopy(d2[k].entries, f2[i2["terms"][k]]) for k in range(len(col_tabs))],
               *[FadeIn(f2[sl]) for sl in i2["plus"]], run_time=1.2)
    scene.play(FadeIn(f2[i2["suffix"]]), run_time=0.5)
    scene.add(f2)
    scene.say("所以 ", "$s_{(1^n)}=e_n$", "：", "$n$", " 次的基本對稱多項式")
    scene.play(FadeIn(g2), ShowCreation(b2), run_time=0.7)
    scene.play(FadeIn(foot), run_time=0.6)
    scene.wait(2.2)


class SceneF03Schur(ChuScene):
    def construct(self):
        self.show_header("Schur 多項式")
        T, tabs, monos, terms, swapped, perm, std_idx, row_tabs, col_tabs = check_math()
        part_monomial(self, T)
        self.clear_stage()
        title, diags, mono_mobs, total, info, extras = part_example(self, tabs, monos, terms, std_idx)
        part_symmetry(self, terms, swapped, perm, title, diags, mono_mobs, total, info, extras)
        self.clear_stage()
        part_h_e(self, row_tabs, col_tabs)
        self.wait(1.0)
