"""
Scene F11 —— Schur 多項式與 Pieri 公式（Fulton《Young Tableaux》§2.2，書 p.24–25）

    S_λ = 表環 R[m] 裡所有 λ 形表的和；T ↦ x^T 把它送到 Schur 多項式 s_λ
        例：λ=(2,1)、m=3 有 8 個表，其中兩個的單項式都是 x1 x2 x3
    Pieri (4) S_λ·S_(p) = Σ S_μ（μ/λ 是 p 格、任兩格不同行＝水平帶）
          (5) S_λ·S_(1^p) = Σ S_μ（任兩格不同列＝垂直帶）
        λ=(2,1)、p=2：水平 (4,1),(3,2),(3,1,1),(2,2,1)；垂直 (3,2),(3,1,1),(2,2,1),(2,1,1,1)
    理由：§1.1 的命題（F05）——T 乘一列 V，新格子一格比一格靠右；每個 U 都唯一地拆成 T·V
        例 T=[[1,2],[2]]、V=1 3 → [[1,1],[2,2]] → [[1,1,3],[2,2]]；m=3 時 8·6 = 48 = 24+15+6+3
    (6) s_λ h_p = Σ s_μ、(7) s_λ e_p = Σ s_μ；m=3 比較 x1²x2²x3 的係數：6 = 2+2+1+1、4 = 2+1+1+0

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF11_pieri.py SceneF11Pieri
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
    content,
    elementary_e,
    insert_word_steps,
    is_horizontal_strip,
    is_vertical_strip,
    kostka,
    pieri_shapes,
    poly_mul,
    poly_sum,
    schur_poly,
    shape,
    skew_boxes,
    ssyt,
    young_boxes,
)

LAM, P, M = (2, 1), 2, 3
H_SHAPES = ((4, 1), (3, 2), (3, 1, 1), (2, 2, 1))           # μ/λ 水平帶
V_SHAPES = ((3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1))     # μ/λ 垂直帶
N_LAM, N_ROW, N_COL = 8, 6, 3                               # m=3 時 λ 形、一列 (2)、一行 (1,1) 的表數
N_H = (24, 15, 6, 3)
N_V = (15, 6, 3, 0)
MONO = (2, 2, 1)                                            # x1² x2² x3
K_H, COEF_H = (2, 2, 1, 1), 6
K_V, COEF_V = (2, 1, 1, 0), 4
T_EX, V_EX = ((1, 2), (2,)), (1, 3)
STAGES_EX = (((1, 1), (2, 2)), ((1, 1, 3), (2, 2)))
NEW_EX = ((1, 1), (0, 2))

H_COLOR, V_COLOR, NEW_COLOR = TEAL, PINK, GREEN
TWIN = (1, 1, 1)                                            # x1 x2 x3：兩個表給同一個單項式


def check_math():
    assert tuple(pieri_shapes(LAM, P)) == H_SHAPES
    assert tuple(pieri_shapes(LAM, P, vertical=True)) == V_SHAPES
    assert all(is_horizontal_strip(mu, LAM) and len(skew_boxes(mu, LAM)) == P for mu in H_SHAPES)
    assert all(is_vertical_strip(mu, LAM) and len(skew_boxes(mu, LAM)) == P for mu in V_SHAPES)
    tabs = ssyt(LAM, M)
    assert len(tabs) == N_LAM
    assert poly_sum({content(T, M): 1} for T in tabs) == schur_poly(LAM, M)
    assert sum(content(T, M) == TWIN for T in tabs) == 2 == schur_poly(LAM, M)[TWIN]
    assert len(ssyt((P,), M)) == N_ROW == len(complete_h(P, M))
    assert len(ssyt((1,) * P, M)) == N_COL == len(elementary_e(P, M))
    assert tuple(len(ssyt(mu, M)) for mu in H_SHAPES) == N_H and N_LAM * N_ROW == sum(N_H) == 48
    assert tuple(len(ssyt(mu, M)) for mu in V_SHAPES) == N_V and N_LAM * N_COL == sum(N_V) == 24
    # (6)(7)：m = 3 時兩邊乘開完全相同
    lhs_h = poly_mul(schur_poly(LAM, M), complete_h(P, M))
    lhs_v = poly_mul(schur_poly(LAM, M), elementary_e(P, M))
    assert lhs_h == poly_sum(schur_poly(mu, M) for mu in H_SHAPES)
    assert lhs_v == poly_sum(schur_poly(mu, M) for mu in V_SHAPES)
    assert lhs_h[MONO] == COEF_H == sum(K_H) and lhs_v[MONO] == COEF_V == sum(K_V)
    assert tuple(kostka(mu, MONO) for mu in H_SHAPES) == K_H
    assert tuple(kostka(mu, MONO) for mu in V_SHAPES) == K_V
    assert tuple(schur_poly(mu, M).get(MONO, 0) for mu in V_SHAPES) == K_V
    assert schur_poly(V_SHAPES[-1], M) == {} and len(V_SHAPES[-1]) == M + 1
    # 理由的例子：T ← 1 ← 3
    steps = insert_word_steps(V_EX, T_EX)
    assert tuple(s[1] for s in steps) == STAGES_EX and tuple(s[3] for s in steps) == NEW_EX
    (r1, c1), (r2, c2) = NEW_EX
    assert c2 > c1 and r2 <= r1                       # 第二格嚴格在右邊、不會更低
    assert shape(STAGES_EX[-1]) in H_SHAPES and set(NEW_EX) == set(skew_boxes(shape(STAGES_EX[-1]), LAM))


def mono_tex(e):
    return "".join(f"x_{k + 1}" if a == 1 else f"x_{k + 1}^{a}" for k, a in enumerate(e) if a)


def s_name(letter, mu):
    return f"{letter}_{{{tuple_str(mu)}}}"


# =============================================================================
# 第 1 段：S_λ 與 Schur 多項式
# =============================================================================
def part_schur(scene):
    tabs = ssyt(LAM, M)
    cs, y_t, y_m = 0.4, 1.2, -0.75
    xs = [-3.25 + 1.33 * k for k in range(len(tabs))]
    defn = mixed("表環 ", "$R[m]$", " 裡：", "$S_\\lambda$", "＝所有 ", "$\\lambda$", " 形、數字在 ",
                 "$[m]$", " 的表的和", font_size=28).move_to(2.6 * UP)
    lab_S = Tex(s_name("S", LAM) + "=", font_size=38).move_to([xs[0] - 0.7, y_t, 0], aligned_edge=RIGHT)
    lab_s = Tex(s_name("s", LAM) + "=", font_size=38).move_to([xs[0] - 0.7, y_m, 0], aligned_edge=RIGHT)
    maps = Tex(r"T\mapsto x^T", font_size=30, fill_color=MUTED_COLOR)
    maps.move_to([lab_S.get_center()[0], (y_t + y_m) / 2, 0])
    tms = VGroup(*[tableau_mob(T, cs, center=np.array([x, y_t, 0.0])) for T, x in zip(tabs, xs)])
    monos = VGroup(*[Tex(mono_tex(content(T, M)), font_size=30).move_to([x, y_m, 0]) for T, x in zip(tabs, xs)])
    plus_t = VGroup(*[Tex("+", font_size=34).move_to([(a + b) / 2, y_t, 0]) for a, b in zip(xs, xs[1:])])
    plus_m = VGroup(*[Tex("+", font_size=34).move_to([(a + b) / 2, y_m, 0]) for a, b in zip(xs, xs[1:])])
    arrows = VGroup(*[Arrow(np.array([x, y_t - 0.5, 0.0]), np.array([x, y_m + 0.32, 0.0]), buff=0.0,
                            thickness=2.0, fill_color=GREY_B) for x in xs])
    twins = [k for k, T in enumerate(tabs) if content(T, M) == TWIN]
    boxes = VGroup(*[SurroundingRectangle(VGroup(tms[k], monos[k]), buff=0.08, color=YELLOW, stroke_width=3)
                     for k in twins])
    note = mixed("$T\\mapsto x^T$", " 是環同態：", "$S_\\lambda$", " 的像就是 Schur 多項式 ", "$s_\\lambda$",
                 font_size=26).move_to(2.15 * DOWN)
    assert_in_frame(defn, lab_S, lab_s, maps, tms, monos, boxes, note)
    assert_apart(defn, VGroup(tms, boxes), gap=0.2)
    assert_apart(note, VGroup(monos, boxes), gap=0.2)
    for a, b in zip(list(tms) + list(monos), list(plus_t) + list(plus_m)):
        assert_apart(a, b, gap=0.05)
    for a, b in zip(list(tms[1:]) + list(monos[1:]), list(plus_t) + list(plus_m)):
        assert_apart(a, b, gap=0.05)
    assert_apart(VGroup(lab_S, lab_s, maps), VGroup(tms, monos), gap=0.2)

    scene.say("在表環 ", "$R[m]$", " 裡，把所有 ", "$\\lambda$", " 形的表加起來，記作 ", "$S_\\lambda$")
    scene.play(FadeIn(defn), run_time=0.7)
    scene.wait(1.3)
    scene.say("例：", "$\\lambda=(2,1)$", "、數字在 1、2、3 裡：一共 ", f"${N_LAM}$", " 個表")
    scene.play(FadeIn(lab_S), LaggedStart(*[FadeIn(t, shift=0.15 * DOWN) for t in tms], lag_ratio=0.15),
               FadeIn(plus_t), run_time=1.6)
    scene.wait(1.0)
    scene.say("每個表換成它的單項式 ", "$x^T$", "（數字 ", "$i$", " 出現幾次，", "$x_i$", " 就幾次方）")
    scene.play(FadeIn(maps), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=1.0)
    scene.play(FadeIn(lab_s), LaggedStart(*[FadeIn(m, shift=0.15 * DOWN) for m in monos], lag_ratio=0.12),
               FadeIn(plus_m), run_time=1.4)
    scene.wait(1.6)
    scene.say("有兩個表都給出 ", "$" + mono_tex(TWIN) + "$", "：合併後它在 ", "$" + s_name("s", LAM) + "$",
              f" 裡的係數是 {schur_poly(LAM, M)[TWIN]}")
    scene.play(ShowCreation(boxes), run_time=0.8)
    scene.play(FadeIn(note, shift=0.15 * UP), run_time=0.7)
    scene.wait(2.2)


# =============================================================================
# 第 2 段：Pieri 公式 (4)(5) 與例子
# =============================================================================
def pieri_row(lhs, shapes, color, y_top, cs=0.34, x_left=-6.3, gap=0.62):
    """VGroup(標籤, 各個圖, 加號, 名稱)；圖頂端對齊在 y_top；新格子（μ/λ）另外記在 .new。"""
    lab = Tex(lhs, font_size=34).move_to([x_left, y_top - cs, 0], aligned_edge=LEFT)
    x = lab.get_right()[0] + 0.35
    diagrams, pluses, names, olds, news = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
    y_name = y_top - max(len(mu) for mu in shapes) * cs - 0.28
    for k, mu in enumerate(shapes):
        if k:
            pluses.add(Tex("+", font_size=34).move_to([x + gap / 2 - 0.05, y_top - cs, 0]))
            x += gap
        d = YoungDiagramMob(mu, cell_size=cs, top_left=np.array([x, y_top, 0.0]))
        new = skew_boxes(mu, LAM)
        d.fill_cells(new, color, opacity=0.8)
        olds.add(d.cell_group(young_boxes(LAM)))
        news.add(d.cell_group(new))
        names.add(Tex(s_name("S", mu), font_size=26, fill_color=MUTED_COLOR).move_to([d.get_center()[0], y_name, 0]))
        diagrams.add(d)
        x = d.get_right()[0]
    out = VGroup(lab, diagrams, pluses, names)
    out.olds, out.news = olds, news
    return out


def part_pieri(scene):
    st4 = mixed("(4)  ", "$S_\\lambda\\cdot S_{(p)}=\\sum S_\\mu$", "：", "$\\mu$", " 由 ", "$\\lambda$",
                " 加 ", "$p$", " 格、任兩格不同行（水平帶）", font_size=26)
    st5 = mixed("(5)  ", "$S_\\lambda\\cdot S_{(1^p)}=\\sum S_\\mu$", "：", "$\\mu$", " 由 ", "$\\lambda$",
                " 加 ", "$p$", " 格、任兩格不同列（垂直帶）", font_size=26)
    st4.move_to([-6.3, 2.75, 0], aligned_edge=LEFT)
    st5.move_to([-6.3, -0.2, 0], aligned_edge=LEFT)
    row_h = pieri_row(s_name("S", LAM) + r"\cdot S_{(2)}=", H_SHAPES, H_COLOR, y_top=2.05)
    row_v = pieri_row(s_name("S", LAM) + r"\cdot S_{(1,1)}=", V_SHAPES, V_COLOR, y_top=-0.9)
    assert_in_frame(st4, st5, row_h, row_v)
    assert_apart(st4, row_h, gap=0.15)
    assert_apart(row_h, st5, gap=0.15)
    assert_apart(st5, row_v, gap=0.15)
    for row in (row_h, row_v):
        for a, b in zip(row[1], row[2]):
            assert_apart(a, b, gap=0.08)
        for a, b in zip(row[1][1:], row[2]):
            assert_apart(a, b, gap=0.08)
        assert_apart(row[0], row[1], gap=0.15)

    scene.say("Pieri 公式 (4)：乘上一列 ", "$S_{(p)}$", "，就是在 ", "$\\lambda$", " 上加一條 ", "$p$",
              " 格的水平帶")
    scene.play(FadeIn(st4), run_time=0.7)
    scene.wait(0.6)
    scene.play(FadeIn(row_h[0]), *[FadeIn(g) for g in row_h.olds], FadeIn(row_h[2]), run_time=0.8)
    scene.say("例：", "$\\lambda=(2,1)$", "、", "$p=2$", "：兩個新格子不能在同一行，共 ",
              f"${len(H_SHAPES)}$", " 種")
    scene.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in row_h.news], lag_ratio=0.25),
               FadeIn(row_h[3]), run_time=1.4)
    scene.wait(2.0)
    scene.say("(5)：乘上一行 ", "$S_{(1^p)}$", "，改成加垂直帶：新格子兩兩不同列")
    scene.play(FadeIn(st5), run_time=0.7)
    scene.wait(0.5)
    scene.play(FadeIn(row_v[0]), *[FadeIn(g) for g in row_v.olds], FadeIn(row_v[2]), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in row_v.news], lag_ratio=0.25),
               FadeIn(row_v[3]), run_time=1.4)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：理由（§1.1 的命題）與計數
# =============================================================================
def part_reason(scene):
    cs, y_top = 0.62, 2.55
    mobs = [tableau_mob(S, cs, top_left=(0, y_top, 0)) for S in (T_EX,) + STAGES_EX]
    xs = (-6.0, -2.9, 0.4)
    for m, x in zip(mobs, xs):
        m.shift((x - m.get_left()[0]) * RIGHT)
    for k, (i, j) in enumerate(NEW_EX):
        for m in mobs[k + 1:]:
            m.cell(i, j).set_fill(NEW_COLOR, opacity=0.45)
    names = VGroup(Tex("T", font_size=36), Tex(r"T\leftarrow 1", font_size=36), Tex(r"T\cdot V", font_size=36))
    y_name = y_top - 2 * cs - 0.35
    for n, m in zip(names, mobs):
        n.move_to([m.get_center()[0], y_name, 0])
    arrows, alabs = VGroup(), VGroup()
    for a, b, x in zip(mobs, mobs[1:], V_EX):
        y = y_top - cs
        arr = Arrow(np.array([a.get_right()[0] + 0.25, y, 0.0]), np.array([b.get_left()[0] - 0.25, y, 0.0]),
                    buff=0.0, thickness=2.5, fill_color=GREY_B)
        arrows.add(arr)
        alabs.add(mixed("插入 ", f"${x}$", font_size=22, color=YELLOW).next_to(arr, UP, buff=0.1))
    U = mobs[-1]
    hop = Arrow(U.cell_center(*NEW_EX[0]), U.cell_center(*NEW_EX[1]), buff=0.2, thickness=3.5, fill_color=YELLOW)
    hop.set_z_index(3)
    vtag = mixed("$V=1\\ 3$", "（一列：弱遞增）", font_size=24).move_to([4.6, y_top - cs, 0])
    lines = VGroup(
        mixed("新格子一格比一格靠右（F05 的命題）", "$\\Rightarrow$", " 兩兩不同行：", "$\\mu/\\lambda$",
              " 是水平帶", font_size=26),
        mixed("反過來：每個這種形狀的 ", "$U$", " 都唯一地拆成 ", "$T\\cdot V$", "（由右往左反向擠出）",
              font_size=26),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    lines.move_to([-6.2, -0.45, 0], aligned_edge=LEFT)
    count = mixed("$m=3$", "：", f"${N_LAM}\\cdot {N_ROW}={N_LAM * N_ROW}="
                  + "+".join(str(n) for n in N_H) + "$", font_size=30)
    sub = zh("（左：T 與 V 的配對數；右：四種 μ 形的表數，" + "、".join(tuple_str(mu) for mu in H_SHAPES) + "）",
             font_size=20, color=MUTED_COLOR)
    block = VGroup(count, sub).arrange(DOWN, buff=0.18).move_to(2.3 * DOWN)
    frame = SurroundingRectangle(block, buff=0.15, color=OK_COLOR, stroke_width=3)
    assert_in_frame(*mobs, names, arrows, alabs, vtag, lines, frame)
    assert_apart(VGroup(*mobs, names, alabs), vtag, gap=0.2)
    assert_apart(VGroup(*mobs, names), lines, gap=0.2)
    assert_apart(lines, frame, gap=0.15)
    for lab, m in zip(alabs, mobs):
        assert_apart(lab, m, gap=0.1)
    for lab, m in zip(alabs, mobs[1:]):
        assert_apart(lab, m, gap=0.1)

    scene.say("為什麼？用 §1.1 的命題：把表 ", "$T$", " 乘上一列 ", "$V$", "（F05）")
    scene.play(FadeIn(mobs[0]), FadeIn(names[0]), FadeIn(vtag), run_time=0.8)
    scene.say("依序插入 1、3：第二個新格子長在第一個的右邊，而且不會更低")
    for k in range(2):
        scene.play(GrowArrow(arrows[k]), FadeIn(alabs[k]), FadeIn(mobs[k + 1], shift=0.2 * RIGHT),
                   FadeIn(names[k + 1]), run_time=0.8)
        scene.wait(0.3)
    scene.play(GrowArrow(hop), run_time=0.6)
    scene.play(FadeIn(lines[0], shift=0.15 * UP), run_time=0.7)
    scene.wait(1.6)
    scene.say("反過來，每個這種形狀的表都唯一地拆成 ", "$T\\cdot V$", "：兩邊的項一一對應")
    scene.play(FadeIn(lines[1], shift=0.15 * UP), run_time=0.7)
    scene.wait(1.2)
    scene.say("數一數 ", "$m=3$", " 的情形：", f"${N_LAM}\\cdot {N_ROW}$", " 對 ", "$(T,V)$", "，恰好是 ",
              f"${N_LAM * N_ROW}$", " 個表")
    scene.play(FadeIn(block), ShowCreation(frame), run_time=0.9)
    scene.wait(2.6)


# =============================================================================
# 第 4 段：(6)(7) 與 m = 3 的驗算
# =============================================================================
def eq_row(lhs, shapes, coefs, total, y, color):
    """「lhs = s_μ1 + s_μ2 + …」以及正下方對齊的係數「total = c1 + c2 + …」。"""
    parts = [Tex(lhs, font_size=36), Tex("=", font_size=36)]
    for k, mu in enumerate(shapes):
        if k:
            parts.append(Tex("+", font_size=36))
        parts.append(Tex(s_name("s", mu), font_size=36))
    top = VGroup(*parts).arrange(RIGHT, buff=0.18).move_to([0, y, 0])
    vals = [str(total), "="] + [s for k, c in enumerate(coefs) for s in ((["+"] if k else []) + [str(c)])]
    bottom = VGroup()
    for p, v in zip(parts, vals):
        bottom.add(Tex(v, font_size=34, fill_color=YELLOW if v not in "=+" else GREY_B)
                   .move_to([p.get_center()[0], y - 0.7, 0]))
    top[0].set_fill(color)
    return top, bottom


def part_poly(scene):
    head = mixed("(6)  ", "$s_\\lambda h_p=\\sum s_\\mu$", "（水平帶）       (7)  ", "$s_\\lambda e_p=\\sum s_\\mu$",
                 "（垂直帶）", font_size=26).move_to(2.65 * UP)
    why = mixed("$T\\mapsto x^T$", "：一列的表加起來是 ", "$h_p$", "，一行的表加起來是 ", "$e_p$",
                font_size=24, color=MUTED_COLOR).move_to(2.0 * UP)
    top_h, bot_h = eq_row(s_name("s", LAM) + "h_2", H_SHAPES, K_H, COEF_H, 0.95, H_COLOR)
    top_v, bot_v = eq_row(s_name("s", LAM) + "e_2", V_SHAPES, K_V, COEF_V, -0.75, V_COLOR)
    key = mixed("黃色：", "$m=3$", " 時兩邊 ", "$" + mono_tex(MONO) + "$", " 的係數（左邊直接把多項式乘開）",
                font_size=24).move_to(2.05 * DOWN)
    zero = mixed("$" + s_name("s", V_SHAPES[-1]) + "$", f" 有 {len(V_SHAPES[-1])} 列，只有 {M} 個變數時是 0",
                 font_size=22, color=MUTED_COLOR).move_to(2.6 * DOWN)
    assert_in_frame(head, why, top_h, bot_h, top_v, bot_v, key, zero)
    for a, b in [(head, why), (why, top_h), (top_h, bot_h), (bot_h, top_v), (top_v, bot_v), (bot_v, key),
                 (key, zero)]:
        assert_apart(a, b, gap=0.12)

    scene.say("把每個表換成 ", "$x^T$", "：(4)(5) 就變成 Schur 多項式的 Pieri 公式")
    scene.play(FadeIn(head), run_time=0.7)
    scene.play(FadeIn(why), run_time=0.6)
    scene.wait(0.5)
    scene.play(FadeIn(top_h), run_time=0.8)
    scene.play(FadeIn(top_v), run_time=0.8)
    scene.wait(0.8)
    scene.say("驗算 ", "$m=3$", "：比較兩邊 ", "$" + mono_tex(MONO) + "$", " 的係數")
    scene.play(FadeIn(key), LaggedStart(*[FadeIn(b, shift=0.1 * DOWN) for b in bot_h], lag_ratio=0.1),
               run_time=1.2)
    scene.wait(1.0)
    scene.play(LaggedStart(*[FadeIn(b, shift=0.1 * DOWN) for b in bot_v], lag_ratio=0.1), run_time=1.2)
    scene.say("最後一項是 0：", "$" + s_name("s", V_SHAPES[-1]) + "$", " 要 4 個不同的數，3 個變數不夠")
    scene.play(FadeIn(zero), Indicate(bot_v[-1], color=RED), run_time=1.0)
    scene.wait(2.5)


class SceneF11Pieri(ChuScene):
    def construct(self):
        self.show_header("Schur 多項式與 Pieri 公式")
        check_math()
        part_schur(self)
        self.clear_stage()
        part_pieri(self)
        self.clear_stage()
        part_reason(self)
        self.clear_stage()
        part_poly(self)
        self.wait(1.0)
